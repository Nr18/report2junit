# Report 2 JUnit

[![Continuous Integration](https://github.com/Nr18/report2junit/actions/workflows/ci.yml/badge.svg)](https://github.com/Nr18/report2junit/actions/workflows/ci.yml)


`report2junit` is a tool that converts various reports into the JUnit format.

## Installation

You can install the `report2junit` tool by running the following command:

```bash
pip install report2junit
```

## Usage

### Syntax

The following syntax can be used to convert a report:

```bash
report2junit --source-type <TYPE> <SOURCE_LOCATION>
```

### Examples

Convert an output report from [cloudformation-guard](https://github.com/aws-cloudformation/cloudformation-guard) using
the following command(s):

```bash
report2junit --source-type cfn-guard ./sample-reports/cfn-guard.json

# Or if you want to specify the destination:
report2junit --source-type cfn-guard ./sample-reports/cfn-guard.json ./sample-reports/cfn-guard-other-destination.xml
```

Convert an output report from [cfn-nag](https://github.com/stelligent/cfn_nag) using
the following command(s):

```bash
report2junit --source-type cfn-nag ./sample-reports/cfn-nag.json

# Or if you want to specify the destination:
report2junit --source-type cfn-nag ./sample-reports/cfn-nag.json ./sample-reports/cfn-nag-other-destination.xml
```

## Releases

 First you will need to update the `version` in the [`pyproject.toml`](./pyproject.toml) file. Then you need to create a
 new release. You can do this by creating a tag and push it to the remote:

 ```bash
 git tag v$(awk '/version/{print $NF}'  pyproject.toml | sed 's/\"//g')
 git push --tags
 ```

 This will trigger the GitHub Actions [`release`](.github/workflows/release.yml) workflow.
