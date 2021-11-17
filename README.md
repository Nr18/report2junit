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
report2junit <SOURCE_LOCATION>
```

### CLI Examples

Convert an output report from [cloudformation-guard][cloudformation-guard] using the following command(s):

```bash
report2junit ./sample-reports/cfn-guard.json

# Or if you want to specify the destination:
report2junit ./sample-reports/cfn-guard.json --destination-file ./sample-reports/cfn-guard-other-destination.xml
```

Convert an output report from [cfn-nag][cfn-nag] using the following command(s):

```bash
report2junit ./sample-reports/cfn-nag.json

# Or if you want to specify the destination:
report2junit ./sample-reports/cfn-nag.json --destination-file ./sample-reports/cfn-nag-other-destination.xml
```

Combine both the [cloudformation-guard][cloudformation-guard] and [cfn-nag][cfn-nag] reports into a single output report.

```bash
report2junit ./sample-reports/cfn-nag.json ./sample-reports/cfn-guard.json

# Or if you want to specify the destination:
report2junit ./sample-reports/cfn-nag.json ./sample-reports/cfn-guard.json --destination-file ./sample-reports/junit-other.xml
```

In some cases it is useful to explicitly stop when there are failures. For example when you want to enforce that there
are no failures. Or on the other hand we could continue when there are failures. This behaviour can be influenced using
the `--ignore-failures` and `--fail-on-failures` options. Where `--fail-on-failures` is the default.

```bash
# Convert the given report and when there are failures exit code 1 is returned.
report2junit ./sample-reports/cfn-guard.json --fail-on-failures
echo $?

# Convert the given report and when there are failures exit code 0 is returned.
report2junit ./sample-reports/cfn-guard.json --ignore-failures
echo $?
```

### AWS CodeBuild Examples

One of the reasons for writing this tool to use it in combination with AWS CodeBuild. In this section you will find a
few examples in how you could use it.

#### Native buildspec.yml

After you synthesized your template, or you use a CloudFormation native template. You can scan it using [cloudformation-guard][cloudformation-guard]
or [cfn-nag][cfn-nag] to scan the template. The outcome of those tools are not compatible with the reporting tools from
AWS CodeBuild. So we will use [report2junit][report2junit] to convert the 2 results into a single, combined compatible
report.

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.8
    commands:
      - pip install -Ur requirements.txt
      - mkdir -p reports
  build:
    commands:
      # Generate the template or use the already existing template.
      - cdk synth > template.yml
      # Use cfn_nag and cfn-guard to scan the generated template
      - cfn_nag_scan --fail-on-warnings --input-path template.yml -o json > reports/cfn-nag.json || true
      - cfn-guard validate --rules cfn-rules.guard --data template.yml --output-format json --show-summary none > reports/cfn-guard.json || true
  post_build:
    commands:
      - report2junit reports/cfn-guard.json reports/cfn-nag.json --destination-file ./reports/combined-junit-report.xml

artifacts:
  files: '**/*'

reports:
  Conpliance:
    base-directory: ./reports
    file-format: JUNITXML
    files:
      - combined-junit-report.xml
```

[cloudformation-guard]: https://github.com/aws-cloudformation/cloudformation-guard "AWS CloudFormation Guard"
[cfn-nag]: https://github.com/stelligent/cfn_nag "Stelligen cfn_nag"
[report2junit]: https://github.com/Nr18/report2junit "Report2JUnit"
