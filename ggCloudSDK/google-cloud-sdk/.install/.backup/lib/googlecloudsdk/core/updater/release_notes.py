# Copyright 2015 Google Inc. All Rights Reserved.

"""Contains utilities for comparing RELEASE_NOTES between Cloud SDK versions.

Example usage:

  old_release_notes = GetReleaseNotes(old_sdk_installation_root)
  new_release_notes = GetReleaseNotes(new_sdk_installation_root)
  for change in ChangesBetween(old_release_notes, new_release_notes):
    print change
"""

import os


class ReleaseNotes(object):
  """Represents a RELEASE_NOTES file.

  Assumes that entries are separated by double-newlines. A typical RELEASE_NOTES
  file would look similar to the following:

    Copyright 2014-2015 Google Inc.
    All Rights Reserved.

    Google Cloud SDK - Release Notes

    1.0.1 (1970/01/02)
    =================
     - Note 3.
     - Note 4.

    1.0.0 (1970/01/01)
    =================
     - Note 1.
     - Note 2.
  """

  def __init__(self, text):
    self.text = text

  @property
  def entries(self):
    return [entry.strip() for entry in self.text.split('\n\n')]

  def __eq__(self, other):
    return self.text == other.text


def GetReleaseNotes(sdk_root):
  """Return a ReleaseNotes instance from inside the given sdk_root.

  If sdk_root is not given or RELEASE_NOTES does not exist in this directory,
  returns None.

  Args:
    sdk_root: str, path to the root of an SDK installation

  Returns:
    ReleaseNotes, release notes object for the given installation
  """
  release_notes_path = os.path.join(sdk_root, 'RELEASE_NOTES')
  if sdk_root and os.path.exists(release_notes_path):
    with open(release_notes_path, 'r') as release_notes_file:
      return ReleaseNotes(release_notes_file.read())
  return None


def ChangesBetween(old_release_notes, new_release_notes):
  """Returns entries present in the new release notes but not the old ones.

  Indented to be used for displaying changes that were made between releases
  (e.g. changes that have been implemented after the previously installed
  version up to and including the latest version in an upgrade).

  Args:
    old_release_notes: ReleaseNotes, the old release notes
    new_release_notes: ReleaseNotes, the new release notes

  Returns:
    list of str, list of entries that were introduced between the old release
      notes and the new release notes
  """
  if old_release_notes is None or new_release_notes is None:
    return []

  changed_entries = []
  for entry in new_release_notes.entries:
    if entry not in old_release_notes.entries:
      changed_entries.append(entry)
  return changed_entries
