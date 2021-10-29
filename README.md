# Report 2 JUnit

[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE.md)
[![Maintenance](https://img.shields.io/badge/Maintained-yes-green.svg)](https://github.com/Nr18/report2junit/graphs/commit-activity)
[![GitHub release](https://img.shields.io/github/release/Nr18/report2junit.svg)](https://github.com/Nr18/report2junit/releases/)
[![Continuous Integration](https://github.com/Nr18/report2junit/actions/workflows/ci.yml/badge.svg)](https://github.com/Nr18/report2junit/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Nr18/report2junit/branch/main/graph/badge.svg?token=RMPJ8DBMKZ)](https://codecov.io/gh/Nr18/report2junit)

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
