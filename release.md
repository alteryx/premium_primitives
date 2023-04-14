# Release Process

## 0. Pre-Release Checklist

Before starting the release process, verify the following:

- All work required for this release has been completed and the team is ready to release.
- [All Github Actions Tests are green on main](https://github.com/alteryx/premium_primitives/actions?query=branch%3Amain).
- Get agreement on the version number to use for the release.

#### Version Numbering

Premium Primitives uses [semantic versioning](https://semver.org/). Every release has a major, minor and patch version number, and are displayed like so: `<majorVersion>.<minorVersion>.<patchVersion>`.

## 1. Create Release on Github

#### Create Release Branch

1. Branch off of premium_primitives main. For the branch name, please use "release_vX.Y.Z" as the naming scheme (e.g. "release_v0.13.3"). Doing so will bypass our release notes checkin test which requires all other PRs to add a release note entry.

#### Bump Version Number

1. Bump `__version__` in `premium_primitives/version.py`, and `premium_primitives/tests/test_version.py`.

#### Update Release Notes

1. Replace "Future Release" in `docs/source/release_notes.rst` with the current date

   ```
   v0.13.3 Sep 28, 2020
   ====================
   ```

2. Remove any unused Release Notes sections for this release (e.g. Fixes, Testing Changes)
3. Add yourself to the list of contributors to this release and **put the contributors in alphabetical order**
4. The release PR does not need to be mentioned in the list of changes
5. Add a commented out "Future Release" section with all of the Release Notes sections above the current section

   ```
   .. Future Release
     ==============
       * Enhancements
       * Fixes
       * Changes
       * Documentation Changes
       * Testing Changes

   .. Thanks to the following people for contributing to this release:
   ```

#### Create Release PR

A [release pr](https://github.com/alteryx/premium_primitives/pull/2) should have **the version number as the title** and the release notes for that release as the PR body text. The contributors list is not necessary. The special sphinx docs syntax (:pr:\`547\`) needs to be changed to github link syntax (#547).

Checklist before merging:

- The title of the PR is the version number.
- All tests are currently green on checkin and on `main`.
- The ReadtheDocs build for the release PR branch has passed, and the resulting docs contain the expected release notes.
- PR has been reviewed and approved.
- Confirm with the team that `main` will be frozen until step 3 (Github Release) is complete.

After merging, verify again that ReadtheDocs "latest" is correct.

## 3. Create Github Release

After the release pull request has been merged into the `main` branch, it is time draft the github release. [Example release](https://github.com/alteryx/premium_primitives/releases/tag/v0.13.3)

- The target should be the `main` branch
- The tag should be the version number with a v prefix (e.g. v0.13.3)
- Release title is the same as the tag
- Release description should be the full Release Notes updates for the release, including the line thanking contributors. Contributors should also have their links changed from the docs syntax (:user:\`gsheni\`) to github syntax (@gsheni)
- This is not a pre-release
- Publishing the release will automatically upload the package to PyPI

## 4. Release on conda-forge

In order to release on conda-forge, you can either wait for a bot to create a pull request, or use a GitHub Actions workflow

### Option a: Use a GitHub Action workflow

1. After the package has been uploaded on PyPI, the **Create Feedstock Pull Request** workflow should automatically kickoff a job.
    * If it does not, go [here](https://github.com/alteryx/premium_primitives/actions/workflows/create_feedstock_pr.yaml)
    * Click **Run workflow** and input the letter `v` followed by the release version (e.g. `v0.13.3`)
    * Kickoff the GitHub Action, and monitor the Job Summary.
2. Once the job has been completed, you will see summary output, with a URL.
    * Visit that URL and create a pull request.
    * Alternatively, create the pull request by clicking the branch name (e.g. - `v0.13.3`):
      - https://github.com/alteryx/premium_primitives-feedstock/branches
3. Verify that the PR has the following:
    * The `build['number']` is 0 (in __recipe/meta.yml__).
    * The `requirements['run']` (in __recipe/meta.yml__) matches the `[project]['dependencies']` in __premium_primitives/pyproject.toml__.
    * The `test['requires']` (in __recipe/meta.yml__) matches the `[project.optional-dependencies]['test']` in __premium_primitives/pyproject.toml__
4. Satisfy the conditions in pull request description and **merge it if the CI passes**.

### Option b: Waiting for bot to create new PR

1. A bot should automatically create a new PR in [conda-forge/premium_primitives-feedstock](https://github.com/conda-forge/premium_primitives-feedstock/pulls) - note, the PR may take up to a few hours to be created
2. Update requirements changes in `recipe/meta.yaml` (bot should have handled version and source links on its own)
3. After tests pass, a maintainer will merge the PR in

# Miscellaneous
## Add new maintainers to premium_primitives-feedstock

Per the instructions [here](https://conda-forge.org/docs/maintainer/updating_pkgs.html#updating-the-maintainer-list):
1. Ask an existing maintainer to create an issue on the [repo](https://github.com/conda-forge/premium_primitives-feedstock).
  a. Select *Bot commands* and put the following title (change `username`):

  ```text
  @conda-forge-admin, please add user @username
  ```

2. A PR will be auto-created on the repo, and will need to be merged by an existing maintainer.
3. The new user will need to **check their email for an invite link to click**, which should be https://github.com/conda-forge
