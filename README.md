# Welcome to imagined.ai's Download Gists Python Script!

We're thrilled to introduce you to our Python script that makes downloading gists from a GitHub user a breeze! Leveraging the power of the GitHub API, it fetches gists and downloads all for a specific user by default! It also provides the flexibility add your GitHub token for higher API limits, to pull gists with a specific file extension, to choose a timeframe based on the created and updated dates, to search on strings the filename may contain, and/or to overwrite existing files or skip them based on your preference! As a bonus, it also neatly compiles the gist's description and metadata into a single file in a common directory. This script is designed to be user-friendly and efficient, making the process of downloading gists as smooth as possible.

## How to Use

To run the script, use the following command:

Here's how you can run the script on Unix, Windows PowerShell, and macOS:

```bash
python3 downloadGists.py <user> --token <token> --extension <extension> --filename <filename> --timeframe_created <YYYY-MM> --timeframe_updated <YYYY-MM> --overwrite
```
Replace `<user>`, `<token>`, `<extension>`, `<filename>`, `<YYYY-MM>` with your actual values. The `--overwrite` flag is optional, as are all of the arguments with the exception of `<user>`.


Here's what each argument does:

- `<user>`: This is a required argument that specifies the GitHub username.
- `<token>`: This is an optional argument that specifies the GitHub access token. If you don't provide this argument, the script will still run, but you might run into rate limits if you make too many requests to the GitHub API in a short period of time. You can create a personal access token by following the instructions at https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token.
- `<extension>`: This is an optional argument that specifies the file extension to download. If you don't provide this argument, the script will download all files.
- `<filename>`: This is an optional argument that specifies a string to search for within filenames. If you provide this argument, the script will download only the files whose names contain the specified string. 
- `<timeframe_created>`: This is an optional argument that filters gists based on when they were created. Provide date in the format: `YYYY-MM-DD` or `YYYY-MM` or `YYYY`.
- `<timeframe_updated>`: This is an optional argument that filters gists based on when they were updated. Provide date in the format: `YYYY-MM-DD` or `YYYY-MM` or `YYYY`.
- `--overwrite`: This is an optional argument that controls whether existing files should be overwritten. If this argument is not provided, the script will skip downloading files that would overwrite existing ones.
Note: Default behavior for all of the above arguments, with the exceptions being `<user>` & `--overwrite`, is to not limit the scope of what gists are being pulled. Case sensitvity applies everywhere!

For example, if you want to download all '.md' files from user 'shaunjohann' that were created in 2023, and you want to overwrite any existing files, you would run:

```bash
python3 downloadGists.py shaunjohann --extension .md --timeframe_created 2023 --overwrite
```

## Rate Limits

As of the time of writing, the GitHub API has a rate limit of 60 requests per hour for unauthenticated requests, and 5000 requests per hour for authenticated requests. However, these limits are subject to change, and you should verify the current rate limits by visiting the [GitHub REST API documentation](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting).

## Acknowledgements

This script was inspired by the work of [leoloobeek](https://gist.github.com/leoloobeek). I would like to express our gratitude for their initial groundwork, which served as a great starting point for this project. You can check out the original gist [here](https://gist.github.com/leoloobeek/3be8b835988e8d926a4387019370db8d).

As someone who doesn't code, I found the process of creating this script to be a challenging but rewarding experience. I want to give a special thanks to [Cursor](https://cursor.so) for their invaluable Chat and Agents features. Their platform made it easy for me to understand and work on this project, and I couldn't have done it without them. I highly recommend checking them out, regardless of experience!

Thank you for helping us make the process of downloading gists easier for everyone!
-SJ @ imagined.ai