# aws-stash

An attempt to make AWS SSM Parameter Store interaction easier and exploit its full potential.

Several tools like [chamber](https://github.com/segmentio/chamber) are already available to provide applications with secrets and other configuration values stored in AWS SSM Parameter Store as environment variables, but they were missing some handy features and flexible output formats, and I was struggling to find any that would also be able to set them.

Usage
-----

```
$ aws-stash --help
usage: aws-stash [-h] [-p PARAMS [PARAMS ...]] [-w [WRITE]] [-m] [-f]
                 [-d DESCRIPTION] [-k KMS] [-c] [-o {text,json,export}] [-l]
                 [-r] [--delete] [-q] [--full] [-v]
                 path

positional arguments:
  path                  Path to the parameter key or folder containing
                        parameter keys

optional arguments:
  -h, --help            show this help message and exit
  -p PARAMS [PARAMS ...], --params PARAMS [PARAMS ...]
                        Parameter keys
  -w [WRITE], --write [WRITE]
                        Write parameter value, leave it empty to input it from
                        STDIN
  -m, --multi-line      Accept multi-line value from STDIN, end input with
                        CTRL+D
  -f, --force           Force overwrite existing value
  -d DESCRIPTION, --description DESCRIPTION
                        Add a description to the parameter
  -k KMS, --kms KMS     KMS key alias to encrypt the value
  -c, --copy            Copy value to the clipboard instead of showing it
  -o {text,json,export}, --output {text,json,export}
                        Output format
  -l, --list            List all paramaters under same level path
  -r, --recursive       Process all paramaters recursively starting from path
  --delete              Delete a single parameter or all parameters
                        recursively starting from path if using --recurise
  -q, --quiet           Output only the values of the parameters
  --full                Output fully qualified parameter path
  -v, --verbose         Output parameters details
```

### AWS credentials

This tool combines nicely with [aws-vault](https://github.com/99designs/aws-vault) to provide AWS credentials in a more secure and convenient way than storing them in `~/.aws/credentials` files.

### List keys recursively

```
$ aws-vault exec my-aws-profile -- aws-stash -r -l /
/dev/
/dev/application-bar/
/dev/application-bar/ENV_VAR_XXX
/dev/application-bar/SECRET_YYY
/dev/application-foo/
/dev/application-foo/ENV_VAR_XXX
/staging/
/staging/application-bar/
/staging/application-bar/ENV_VAR_XXX
/staging/application-bar/SECRET_YYY
/staging/application-foo/
/staging/application-foo/ENV_VAR_ZZZ
```

Installation from source
------------------------

```
git clone https://github.com/askainet/aws-stash
pip install aws-stash/
```
