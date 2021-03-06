"""Generated client library for cloudresourcemanager version v1beta1."""
# NOTE: This file is autogenerated and should not be edited by hand.

from googlecloudsdk.third_party.apitools.base.py import base_api
from googlecloudsdk.third_party.apis.cloudresourcemanager.v1beta1 import cloudresourcemanager_v1beta1_messages as messages


class CloudresourcemanagerV1beta1(base_api.BaseApiClient):
  """Generated client library for service cloudresourcemanager version v1beta1."""

  MESSAGES_MODULE = messages

  _PACKAGE = u'cloudresourcemanager'
  _SCOPES = [u'https://www.googleapis.com/auth/cloud-platform']
  _VERSION = u'v1beta1'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = ''
  _CLIENT_CLASS_NAME = u'CloudresourcemanagerV1beta1'
  _URL_VERSION = u'v1beta1'

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None):
    """Create a new cloudresourcemanager handle."""
    url = url or u'https://cloudresourcemanager.googleapis.com/'
    super(CloudresourcemanagerV1beta1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers)
    self.organizations = self.OrganizationsService(self)
    self.projects = self.ProjectsService(self)

  class OrganizationsService(base_api.BaseApiService):
    """Service class for the organizations resource."""

    _NAME = u'organizations'

    def __init__(self, client):
      super(CloudresourcemanagerV1beta1.OrganizationsService, self).__init__(client)
      self._method_configs = {
          'Get': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'cloudresourcemanager.organizations.get',
              ordered_params=[u'organizationId'],
              path_params=[u'organizationId'],
              query_params=[],
              relative_path=u'v1beta1/organizations/{organizationId}',
              request_field='',
              request_type_name=u'CloudresourcemanagerOrganizationsGetRequest',
              response_type_name=u'Organization',
              supports_download=False,
          ),
          'GetIamPolicy': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'cloudresourcemanager.organizations.getIamPolicy',
              ordered_params=[u'resource'],
              path_params=[u'resource'],
              query_params=[],
              relative_path=u'v1beta1/organizations/{resource}:getIamPolicy',
              request_field=u'getIamPolicyRequest',
              request_type_name=u'CloudresourcemanagerOrganizationsGetIamPolicyRequest',
              response_type_name=u'Policy',
              supports_download=False,
          ),
          'List': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'cloudresourcemanager.organizations.list',
              ordered_params=[],
              path_params=[],
              query_params=[u'filter', u'pageSize', u'pageToken'],
              relative_path=u'v1beta1/organizations',
              request_field='',
              request_type_name=u'CloudresourcemanagerOrganizationsListRequest',
              response_type_name=u'ListOrganizationsResponse',
              supports_download=False,
          ),
          'SetIamPolicy': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'cloudresourcemanager.organizations.setIamPolicy',
              ordered_params=[u'resource'],
              path_params=[u'resource'],
              query_params=[],
              relative_path=u'v1beta1/organizations/{resource}:setIamPolicy',
              request_field=u'setIamPolicyRequest',
              request_type_name=u'CloudresourcemanagerOrganizationsSetIamPolicyRequest',
              response_type_name=u'Policy',
              supports_download=False,
          ),
          'TestIamPermissions': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'cloudresourcemanager.organizations.testIamPermissions',
              ordered_params=[u'resource'],
              path_params=[u'resource'],
              query_params=[],
              relative_path=u'v1beta1/organizations/{resource}:testIamPermissions',
              request_field=u'testIamPermissionsRequest',
              request_type_name=u'CloudresourcemanagerOrganizationsTestIamPermissionsRequest',
              response_type_name=u'TestIamPermissionsResponse',
              supports_download=False,
          ),
          'Update': base_api.ApiMethodInfo(
              http_method=u'PUT',
              method_id=u'cloudresourcemanager.organizations.update',
              ordered_params=[u'organizationId'],
              path_params=[u'organizationId'],
              query_params=[],
              relative_path=u'v1beta1/organizations/{organizationId}',
              request_field='<request>',
              request_type_name=u'Organization',
              response_type_name=u'Organization',
              supports_download=False,
          ),
          }

      self._upload_configs = {
          }

    def Get(self, request, global_params=None):
      """Fetches an Organization resource by id.

      Args:
        request: (CloudresourcemanagerOrganizationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Organization) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    def GetIamPolicy(self, request, global_params=None):
      """Gets the access control policy for a Organization resource. May be empty if.
no such policy or resource exists.

      Args:
        request: (CloudresourcemanagerOrganizationsGetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('GetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    def List(self, request, global_params=None):
      """Query Organization resources.

      Args:
        request: (CloudresourcemanagerOrganizationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListOrganizationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    def SetIamPolicy(self, request, global_params=None):
      """Sets the access control policy on a Organization resource. Replaces any.
existing policy.

      Args:
        request: (CloudresourcemanagerOrganizationsSetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('SetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    def TestIamPermissions(self, request, global_params=None):
      """Returns permissions that a caller has on the specified Organization.

      Args:
        request: (CloudresourcemanagerOrganizationsTestIamPermissionsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (TestIamPermissionsResponse) The response message.
      """
      config = self.GetMethodConfig('TestIamPermissions')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Update(self, request, global_params=None):
      """Updates an Organization resource.

      Args:
        request: (Organization) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Organization) The response message.
      """
      config = self.GetMethodConfig('Update')
      return self._RunMethod(
          config, request, global_params=global_params)

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = u'projects'

    def __init__(self, client):
      super(CloudresourcemanagerV1beta1.ProjectsService, self).__init__(client)
      self._method_configs = {
          'Create': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'cloudresourcemanager.projects.create',
              ordered_params=[],
              path_params=[],
              query_params=[],
              relative_path=u'v1beta1/projects',
              request_field='<request>',
              request_type_name=u'Project',
              response_type_name=u'Project',
              supports_download=False,
          ),
          'Delete': base_api.ApiMethodInfo(
              http_method=u'DELETE',
              method_id=u'cloudresourcemanager.projects.delete',
              ordered_params=[u'projectId'],
              path_params=[u'projectId'],
              query_params=[],
              relative_path=u'v1beta1/projects/{projectId}',
              request_field='',
              request_type_name=u'CloudresourcemanagerProjectsDeleteRequest',
              response_type_name=u'Empty',
              supports_download=False,
          ),
          'Get': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'cloudresourcemanager.projects.get',
              ordered_params=[u'projectId'],
              path_params=[u'projectId'],
              query_params=[],
              relative_path=u'v1beta1/projects/{projectId}',
              request_field='',
              request_type_name=u'CloudresourcemanagerProjectsGetRequest',
              response_type_name=u'Project',
              supports_download=False,
          ),
          'GetIamPolicy': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'cloudresourcemanager.projects.getIamPolicy',
              ordered_params=[u'resource'],
              path_params=[u'resource'],
              query_params=[],
              relative_path=u'v1beta1/projects/{resource}:getIamPolicy',
              request_field=u'getIamPolicyRequest',
              request_type_name=u'CloudresourcemanagerProjectsGetIamPolicyRequest',
              response_type_name=u'Policy',
              supports_download=False,
          ),
          'List': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'cloudresourcemanager.projects.list',
              ordered_params=[],
              path_params=[],
              query_params=[u'filter', u'pageSize', u'pageToken'],
              relative_path=u'v1beta1/projects',
              request_field='',
              request_type_name=u'CloudresourcemanagerProjectsListRequest',
              response_type_name=u'ListProjectsResponse',
              supports_download=False,
          ),
          'SetIamPolicy': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'cloudresourcemanager.projects.setIamPolicy',
              ordered_params=[u'resource'],
              path_params=[u'resource'],
              query_params=[],
              relative_path=u'v1beta1/projects/{resource}:setIamPolicy',
              request_field=u'setIamPolicyRequest',
              request_type_name=u'CloudresourcemanagerProjectsSetIamPolicyRequest',
              response_type_name=u'Policy',
              supports_download=False,
          ),
          'TestIamPermissions': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'cloudresourcemanager.projects.testIamPermissions',
              ordered_params=[u'resource'],
              path_params=[u'resource'],
              query_params=[],
              relative_path=u'v1beta1/projects/{resource}:testIamPermissions',
              request_field=u'testIamPermissionsRequest',
              request_type_name=u'CloudresourcemanagerProjectsTestIamPermissionsRequest',
              response_type_name=u'TestIamPermissionsResponse',
              supports_download=False,
          ),
          'Undelete': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'cloudresourcemanager.projects.undelete',
              ordered_params=[u'projectId'],
              path_params=[u'projectId'],
              query_params=[],
              relative_path=u'v1beta1/projects/{projectId}:undelete',
              request_field='',
              request_type_name=u'CloudresourcemanagerProjectsUndeleteRequest',
              response_type_name=u'Empty',
              supports_download=False,
          ),
          'Update': base_api.ApiMethodInfo(
              http_method=u'PUT',
              method_id=u'cloudresourcemanager.projects.update',
              ordered_params=[u'projectId'],
              path_params=[u'projectId'],
              query_params=[],
              relative_path=u'v1beta1/projects/{projectId}',
              request_field='<request>',
              request_type_name=u'Project',
              response_type_name=u'Project',
              supports_download=False,
          ),
          }

      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      """Creates a project resource.

Initially, the project resource is owned by its creator exclusively.
The creator can later grant permission to others to read or update the
project.

Several APIs are activated automatically for the project, including
Google Cloud Storage.

      Args:
        request: (Project) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Project) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Delete(self, request, global_params=None):
      """Marks the project identified by the specified.
`project_id` (for example, `my-project-123`) for deletion.
This method will only affect the project if the following criteria are met:

+ The project does not have a billing account associated with it.
+ The project has a lifecycle state of
ACTIVE.

This method changes the project's lifecycle state from
ACTIVE
to DELETE_REQUESTED.
The deletion starts at an unspecified time,
at which point the lifecycle state changes to DELETE_IN_PROGRESS.

Until the deletion completes, you can check the lifecycle state
checked by retrieving the project with GetProject,
and the project remains visible to ListProjects.
However, you cannot update the project.

After the deletion completes, the project is not retrievable by
the  GetProject and
ListProjects methods.

The caller must have modify permissions for this project.

      Args:
        request: (CloudresourcemanagerProjectsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Get(self, request, global_params=None):
      """Retrieves the project identified by the specified.
`project_id` (for example, `my-project-123`).

The caller must have read permissions for this project.

      Args:
        request: (CloudresourcemanagerProjectsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Project) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    def GetIamPolicy(self, request, global_params=None):
      """Returns the IAM access control policy for specified project.

      Args:
        request: (CloudresourcemanagerProjectsGetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('GetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    def List(self, request, global_params=None):
      """Lists projects that are visible to the user and satisfy the.
specified filter. This method returns projects in an unspecified order.
New projects do not necessarily appear at the end of the list.

      Args:
        request: (CloudresourcemanagerProjectsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListProjectsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    def SetIamPolicy(self, request, global_params=None):
      """Sets the IAM access control policy for the specified project. We do not.
currently support 'domain:' prefixed members in a Binding of a Policy.

Calling this method requires enabling the App Engine Admin API.

      Args:
        request: (CloudresourcemanagerProjectsSetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('SetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    def TestIamPermissions(self, request, global_params=None):
      """Tests the specified permissions against the IAM access control policy.
for the specified project.

      Args:
        request: (CloudresourcemanagerProjectsTestIamPermissionsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (TestIamPermissionsResponse) The response message.
      """
      config = self.GetMethodConfig('TestIamPermissions')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Undelete(self, request, global_params=None):
      """Restores the project identified by the specified.
`project_id` (for example, `my-project-123`).
You can only use this method for a project that has a lifecycle state of
DELETE_REQUESTED.
After deletion starts, as indicated by a lifecycle state of
DELETE_IN_PROGRESS,
the project cannot be restored.

The caller must have modify permissions for this project.

      Args:
        request: (CloudresourcemanagerProjectsUndeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Undelete')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Update(self, request, global_params=None):
      """Updates the attributes of the project identified by the specified.
`project_id` (for example, `my-project-123`).

The caller must have modify permissions for this project.

      Args:
        request: (Project) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Project) The response message.
      """
      config = self.GetMethodConfig('Update')
      return self._RunMethod(
          config, request, global_params=global_params)
