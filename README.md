# Report 2 JUnit

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