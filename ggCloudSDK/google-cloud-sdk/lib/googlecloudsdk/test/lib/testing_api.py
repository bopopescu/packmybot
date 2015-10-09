# Copyright 2014 Google Inc. All Rights Reserved.

"""A shared library to support implementation of Cloud Test Lab commands."""

import collections
import os
import time

from googlecloudsdk.calliope import exceptions
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core.console import console_io
from googlecloudsdk.third_party.apitools.base import py as apitools_base

from googlecloudsdk.test.lib import exit_code
from googlecloudsdk.test.lib import util


DEFAULT_STATUS_INTERVAL_SECS = 6.0


class TestingApiHelper(object):
  """A utility class to encapsulate common Testing API operations."""

  def __init__(self, project, args, history_id, gcs_results_root,
               testing_client, testing_messages):
    """Construct a TestingApiHelper to be used with a single test invocation.

    Args:
      project: string containing the GCE project id.
      args: an argparse namespace. All the arguments that were provided to this
        command invocation (i.e. group and command arguments combined).
      history_id: A history ID string to publish Tool Results to.
      gcs_results_root: the root dir for a matrix within the GCS results bucket.
      testing_client: Testing API client lib generated by Apitools.
      testing_messages: Testing API messages lib generated by Apitools.
    """
    self._project = project
    self._args = args
    self._history_id = history_id
    self._gcs_results_root = gcs_results_root
    self._client = testing_client
    self._messages = testing_messages
    self._max_status_length = 0

    self.status_interval_sec = (
        properties.VALUES.test.matrix_status_interval.GetInt() or
        DEFAULT_STATUS_INTERVAL_SECS)
    # Poll the matrix status half as fast if not running in interactive mode.
    if not console_io.IsInteractive(error=True):
      self.status_interval_sec *= 2
    log.info('Matrix status interval: {0} sec'.format(self.status_interval_sec))

    exec_states = testing_messages.TestExecution.StateValueValuesEnum
    self.state_names = {
        exec_states.VALIDATING: 'Validating',
        exec_states.PENDING: 'Pending',
        exec_states.RUNNING: 'Running',
        exec_states.FINISHED: 'Finished',
        exec_states.ERROR: 'Error',
        exec_states.UNSUPPORTED_ENVIRONMENT: 'Unsupported',
        exec_states.INCOMPATIBLE_ENVIRONMENT: 'Incompatible Environment',
        exec_states.INCOMPATIBLE_ARCHITECTURE: 'Incompatible Architecture',
        exec_states.CANCELLED: 'Cancelled',
        exec_states.INVALID: 'Invalid',
        exec_states.TEST_STATE_UNSPECIFIED: '*Unspecified*',
    }
    self.completed_execution_states = set([
        exec_states.FINISHED,
        exec_states.ERROR,
        exec_states.UNSUPPORTED_ENVIRONMENT,
        exec_states.INCOMPATIBLE_ENVIRONMENT,
        exec_states.INCOMPATIBLE_ARCHITECTURE,
        exec_states.CANCELLED,
        exec_states.INVALID,
    ])
    matrix_states = testing_messages.TestMatrix.StateValueValuesEnum
    self.completed_matrix_states = set([
        matrix_states.FINISHED,
        matrix_states.ERROR,
        matrix_states.CANCELLED,
        matrix_states.INVALID,
    ])

  def _BuildApkFileReference(self, apk):
    """Build a FileReference message pointing to the GCS copy of an APK file."""
    return self._messages.FileReference(
        gcsPath=os.path.join(self._gcs_results_root, os.path.basename(apk)))

  def _BuildAndroidInstrumentationTestSpec(self):
    """Build a TestSpecification for an AndroidInstrumentationTest."""
    test = self._messages.AndroidInstrumentationTest(
        appApk=self._BuildApkFileReference(self._args.app),
        testApk=self._BuildApkFileReference(self._args.test),
        appPackageId=self._args.app_package,
        testPackageId=self._args.test_package,
        testRunnerClass=self._args.test_runner_class,
        testTargets=(self._args.test_targets or []))
    return self._messages.TestSpecification(
        androidInstrumentationTest=test,
        testTimeout=self._args.timeout)

  def _BuildAndroidMonkeyTestSpec(self):
    """Build a TestSpecification for an AndroidMonkeyTest."""
    test = self._messages.AndroidMonkeyTest(
        appApk=self._BuildApkFileReference(self._args.app),
        appPackageId=self._args.app_package,
        eventCount=self._args.event_count,
        eventDelay='{0:.3f}s'.format(self._args.event_delay/1000.0),
        randomSeed=self._args.random_seed)
    return self._messages.TestSpecification(
        androidMonkeyTest=test,
        testTimeout=self._args.timeout)

  def _BuildAndroidRoboTestSpec(self):
    """Build a TestSpecification for an AndroidRoboTest."""
    test = self._messages.AndroidRoboTest(
        appApk=self._BuildApkFileReference(self._args.app),
        appPackageId=self._args.app_package,
        maxDepth=self._args.max_depth,
        maxSteps=self._args.max_steps,
        appInitialActivity=self._args.app_initial_activity)
    return self._messages.TestSpecification(
        androidRoboTest=test,
        testTimeout=self._args.timeout)

  def _TestSpecFromType(self, test_type):
    """Map a test type into its corresponding TestSpecification message ."""
    if test_type == 'instrumentation':
      return self._BuildAndroidInstrumentationTestSpec()
    elif test_type == 'monkey':
      return self._BuildAndroidMonkeyTestSpec()
    elif test_type == 'robo':
      return self._BuildAndroidRoboTestSpec()
    else:  # It's a bug in our arg validation if we ever get here.
      raise exceptions.InvalidArgumentException(
          'type', 'Unknown test type "{}".'.format(test_type))

  def _BuildTestMatrix(self, spec):
    """Build just the user-specified parts of a TestMatrix message.

    Args:
      spec: a TestSpecification message corresponding to the test type.

    Returns:
      A TestMatrix message.
    """
    android_matrix = self._messages.AndroidMatrix(
        androidModelIds=self._args.device_ids,
        androidVersionIds=self._args.os_version_ids,
        locales=self._args.locales,
        orientations=self._args.orientations)

    gcs = self._messages.GoogleCloudStorage(gcsPath=self._gcs_results_root)
    hist = self._messages.ToolResultsHistory(projectId=self._project,
                                             historyId=self._history_id)
    results = self._messages.ResultStorage(googleCloudStorage=gcs,
                                           toolResultsHistory=hist)

    return self._messages.TestMatrix(
        testSpecification=spec,
        environmentMatrix=self._messages.EnvironmentMatrix(
            androidMatrix=android_matrix),
        clientInfo=self._messages.ClientInfo(name='gcloud'),
        resultStorage=results)

  def _BuildTestMatrixRequest(self):
    """Build a TestingProjectsTestMatricesCreateRequest for a test matrix.

    Returns:
      A TestingProjectsTestMatricesCreateRequest message.
    """
    spec = self._TestSpecFromType(self._args.type)
    return self._messages.TestingProjectsTestMatricesCreateRequest(
        projectId=self._project,
        testMatrix=self._BuildTestMatrix(spec))

  def CreateTestMatrix(self):
    """Invoke the Testing service to create a test matrix from the user's args.

    Returns:
      The TestMatrix response message from the TestMatrices.Create rpc.

    Raises:
      HttpException if the test service reports an HttpError.
    """
    request = self._BuildTestMatrixRequest()
    log.debug('TestMatrices.Create request:\n{0}\n'.format(request))
    try:
      response = self._client.projects_testMatrices.Create(request)
      log.debug('TestMatrices.Create response:\n{0}\n'.format(response))
    except apitools_base.HttpError as error:
      log.debug(
          'TestMatrices.Create reported HttpError:\n{0}'.format(error))
      raise exceptions.HttpException(util.GetError(error))

    log.status.Print('Test [{id}] has been created in the Google Cloud.'
                     .format(id=response.testMatrixId))
    return response

  def CancelTestMatrix(self, matrix_id):
    """Cancels an in-progress TestMatrix.

    Args:
      matrix_id: str, the unique id of the test matrix to be cancelled.

    Raises:
      HttpException if the Test service reports a back-end error.
    """
    request = self._messages.TestingProjectsTestMatricesCancelRequest(
        projectId=self._project,
        testMatrixId=matrix_id)
    try:
      self._client.projects_testMatrices.Cancel(request)
    except apitools_base.HttpError as error:
      msg = 'Http error from CancelTestMatrix: ' + util.GetError(error)
      raise exceptions.HttpException(msg)

  def HandleUnsupportedExecutions(self, matrix):
    """Report unsupported device dimensions and return supported test list.

    Args:
      matrix: a TestMatrix message.

    Returns:
      A list of TestExecution messages which have supported dimensions.
    """
    states = self._messages.TestExecution.StateValueValuesEnum
    supported_tests = []
    unsupported_dimensions = set()

    for test in matrix.testExecutions:
      if test.state == states.UNSUPPORTED_ENVIRONMENT:
        unsupported_dimensions.add(_GetInvalidDimensionString(test.environment))
      else:
        supported_tests.append(test)

    if unsupported_dimensions:
      log.status.Print(
          'Some device dimensions are not compatible and will be skipped: {d}'
          .format(d=' '.join(unsupported_dimensions)))
    log.status.Print(
        'Cloud Test Lab will execute your {t} test on {n} device(s).'
        .format(t=self._args.type, n=len(supported_tests)))
    return supported_tests

  def _GetTestExecutionStatus(self, matrix_id, test_id):
    """Fetch the TestExecution state of a specific test within a matrix."""
    matrix = self.GetTestMatrixStatus(matrix_id)
    for test in matrix.testExecutions:
      if test.id == test_id:
        return test
    raise exceptions.ToolException(   # We should never get here.
        'Error: test [{0}] not found in matrix [{1}].'.format(
            test_id, matrix_id))

  def MonitorTestExecutionProgress(self, matrix_id, test_id):
    """Monitor and report the progress of a single running test.

    This method prints more detailed test progress messages for the case where
    the matrix has exactly one supported test configuration.

    Args:
      matrix_id: str, the unique id of the test matrix to be monitored.
      test_id: str, the unique id of the single supported test in the matrix.

    Raises:
      ToolException if the Test service reports a backend error.
    """
    states = self._messages.TestExecution.StateValueValuesEnum
    last_state = ''
    error = ''
    progress = []
    last_progress_len = 0

    while True:
      status = self._GetTestExecutionStatus(matrix_id, test_id)
      # Check for optional error and progress details
      details = status.testDetails
      if details:
        error = details.errorMessage or ''
        progress = details.progressMessages or []

      # Progress is cumulative, so only print what's new since the last update.
      for msg in progress[last_progress_len:]:
        log.status.Print(msg.rstrip())
      last_progress_len = len(progress)

      if status.state == states.ERROR:
        raise exceptions.ToolException(
            'Cloud Test Lab infrastructure failure: {e}'.format(e=error),
            exit_code=exit_code.INFRASTRUCTURE_ERR)

      if status.state == states.UNSUPPORTED_ENVIRONMENT:
        msg = ('Device dimensions are not compatible: {d}. '
               'Please use "gcloud alpha test android devices list" to '
               'determine which device dimensions are compatible.'
               .format(d=_GetInvalidDimensionString(status.environment)))
        raise exceptions.ToolException(msg, exit_code=exit_code.UNSUPPORTED_ENV)

      # Inform user of test progress, typically PENDING -> RUNNING -> FINISHED
      if status.state != last_state:
        log.status.Print('Test is {s}'.format(s=self.state_names[status.state]))
        last_state = status.state

      if status.state in self.completed_execution_states:
        break

      self._SleepForStatusInterval()

    # Even if the single TestExecution is done, we also need to wait for the
    # matrix to reach a finalized state before monitoring is done.
    matrix = self.GetTestMatrixStatus(matrix_id)
    while matrix.state not in self.completed_matrix_states:
      log.debug('Matrix not yet complete, still in state: %s', matrix.state)
      self._SleepForStatusInterval()
      matrix = self.GetTestMatrixStatus(matrix_id)
    self._LogTestComplete(matrix.state)
    return

  def GetTestMatrixStatus(self, matrix_id):
    """Fetch the response from the GetTestMatrix rpc.

    Args:
      matrix_id: str, the unique id of the test matrix to be polled.

    Returns:
      A TestMatrix message holding the current state of the created tests.

    Raises:
      HttpException if the Test service reports a backend error.
    """
    request = self._messages.TestingProjectsTestMatricesGetRequest(
        projectId=self._project,
        testMatrixId=matrix_id)
    try:
      return self._client.projects_testMatrices.Get(request)
    except apitools_base.HttpError as error:
      msg = 'Http error while monitoring test run: ' + util.GetError(error)
      raise exceptions.HttpException(msg)

  def MonitorTestMatrixProgress(self, matrix_id):
    """Monitor and report the progress of multiple running tests in a matrix.

    Args:
      matrix_id: str, the unique id of the test matrix to be monitored.
    """
    state_counts = {}
    while True:
      matrix = self.GetTestMatrixStatus(matrix_id)

      state_counts = collections.defaultdict(int)
      for test in matrix.testExecutions:
        state_counts[test.state] += 1

      self._UpdateMatrixStatus(state_counts)

      if matrix.state in self.completed_matrix_states:
        self._LogTestComplete(matrix.state)
        break
      self._SleepForStatusInterval()

  def _UpdateMatrixStatus(self, state_counts):
    """Update the matrix status line with the current test state counts.

    Example: 'Test matrix status: Finished:5 Running:3 Unsupported:2'

    Args:
      state_counts: {state:count} a dict mapping a test state to its frequency.
    """
    status = []
    for state, count in state_counts.iteritems():
      if count > 0:
        status.append('{s}:{c}'.format(s=self.state_names[state], c=count))
    status.sort()
    # Use \r so that the status summary will update on the same console line.
    out = '\rTest matrix status: {0} '.format(' '.join(status))

    # Right-pad with blanks when the status line gets shorter.
    self._max_status_length = max(len(out), self._max_status_length)
    log.status.write(out.ljust(self._max_status_length))

  def _LogTestComplete(self, matrix_state):
    """Let the user know that their test matrix has completed running."""
    log.info('Test matrix completed in state: {0}'.format(matrix_state))
    log.status.Print('\n{0} testing complete.'
                     .format(self._args.type.capitalize()))

  def _SleepForStatusInterval(self):
    time.sleep(self.status_interval_sec)


def _GetInvalidDimensionString(environment):
  if hasattr(environment, 'androidDevice'):
    device = environment.androidDevice
    return ('[OS-version {vers} on {model}]'
            .format(model=device.androidModelId, vers=device.androidVersionId))
  else:
    # TODO(user): handle other device environments here (e.g. iOS).
    return '[unknown-environment]'
