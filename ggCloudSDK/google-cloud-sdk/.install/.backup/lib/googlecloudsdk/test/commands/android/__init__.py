# Copyright 2014 Google Inc. All Rights Reserved.

"""The 'gcloud test android' sub-group."""

from googlecloudsdk.calliope import base

from googlecloudsdk.test.lib import util


class Android(base.Group):
  """Command group for Android application testing."""

  detailed_help = {
      'DESCRIPTION': """\
          Explore physical and virtual Android devices and Android OS versions
          which are available as test targets. Also run tests against your
          Android app on these devices, monitor your test progress, and view
          detailed test results in the Google Developers Console.
          """,

      'EXAMPLES': """\
          To see a list of available Android devices, their form factors, and
          supported Android OS versions, run:

            $ {command} devices list

          To view all options available for running Android tests, run:

            $ {command} run --help
      """
  }

  @staticmethod
  def Args(parser):
    """Method called by Calliope to register flags common to this sub-group.

    Args:
      parser: An argparse parser used to add arguments that immediately follow
          this group in the CLI. Positional arguments are allowed.
    """

  def Filter(self, context, args):
    """Modify the context that will be given to this group's commands when run.

    Args:
      context: {str:object}, The current context, which is a set of key-value
          pairs that can be used for common initialization among commands.
      args: argparse.Namespace: The same Namespace given to the corresponding
          .Run() invocation.

    Returns:
      The refined command context.
    """
    # Get the android catalog and store in the context
    context['android_catalog'] = util.GetAndroidCatalog(context)
    return context
