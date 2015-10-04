# Copyright 2013 Google Inc. All Rights Reserved.

"""The command to list installed/available gcloud components."""

from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core.console import console_io
from googlecloudsdk.core.updater import update_manager

from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions


class Remove(base.Command):
  """Remove a registered Trusted Test component repository.
  """
  detailed_help = {
      'DESCRIPTION': """\
          Remove a registered Trusted Tester component repository from the list
          of repositories used by the component manager.  After removing a
          repository, you can run:
            $ gcloud components update
          to revert back to the standard version of any components that were
          installed from that repository.
      """,
      'EXAMPLES': """\
          To be prompted for registered Trusted Tester component repositories to
          remove run:

            $ gcloud components repositories remove
      """,
  }

  @staticmethod
  def Args(parser):
    url_arg = parser.add_argument(
        'url',
        nargs='*',
        metavar='URL',
        help='Zero or more URLs for the component repositories you want to '
        'remove.  If none are given, you will be prompted to choose which '
        'existing repository you want to remove.')
    url_arg.completer = Remove.group_class.RepoCompleter
    parser.add_argument('--all', action='store_true',
                        help='Remove all registered repositories.')

  def Run(self, args):
    """Runs the remove command."""
    repos = update_manager.UpdateManager.GetAdditionalRepositories()
    removed_repos = []

    # Removing all URLs.
    if args.all:
      removed_repos.extend(repos)
      repos = []

    # Specifying URLs to remove explicitly.
    elif args.url:
      if not repos:
        raise exceptions.ToolException('You have no registered repositories.')
      for url in args.url:
        if url not in repos:
          raise exceptions.ToolException(
              'URL [{0}] was not a known registered repository.'.format(url))
      for url in args.url:
        repos.remove(url)
      removed_repos.extend(args.url)

    # No URL specified, prompt to choose one.
    else:
      if not repos:
        raise exceptions.ToolException('You have no registered repositories.')
      result = console_io.PromptChoice(
          repos, default=None,
          message='Which repository would you like to remove?')
      if result is None:
        log.status.Print('No repository was removed.')
      else:
        removed_repos.append(repos.pop(result))

    if removed_repos:
      properties.PersistProperty(
          properties.VALUES.component_manager.additional_repositories,
          ','.join(repos) if repos else None,
          scope=properties.Scope.INSTALLATION)

    for removed_repo in removed_repos:
      log.status.Print('Removed repository: [{repo}]'.format(repo=removed_repo))
    return removed_repos

  def Display(self, unused_args, unused_removed_repos):
    # Don't print anything by default.
    pass
