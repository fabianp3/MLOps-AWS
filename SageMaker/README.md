This error has also been observed when SageMaker Canvas user permissions do not allow access to a file. While users can select the file, I recall that by default, buckets prefixed with 'sagemaker' are configured for access, whereas other buckets may require additional configuration.

It might be worth trying to move the file to an S3 bucket that starts with 'sagemaker' to see if that helps identify the source of the issue.



organizarlo
