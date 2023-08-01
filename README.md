## 📌 Introducing imagined.ai's Python Script for Gist Downloads

We are delighted to unveil our user-friendly Python script designed for an effortless experience downloading gists from any GitHub user! Using the GitHub API, this script automatically fetches and downloads all gists from a given user by default. 

It offers extensive customization, allowing you to use your GitHub token for improved API limits, filter gists based on file extensions or filename strings, specify a time range according to creation or update dates, and decide whether to overwrite or skip existing files. As an added convenience, all metadata and descriptions from each gist are neatly compiled into a single file within a common directory. 

## User Guide

You can execute the script on Unix, Windows PowerShell, and macOS using the following command:

```bash
python3 downloadGists.py <user> --token <token> --extension <extension> --filename <filename> --timeframe_created <YYYY-MM> --timeframe_updated <YYYY-MM> --overwrite
```

Ensure to replace `<user>`, `<token>`, `<extension>`, `<filename>`, `<YYYY-MM>` with your actual values. The `--overwrite` flag is optional and so are the other arguments, apart from `<user>`. 

Here's an explanation of each argument:

- `<user>`: (Mandatory) Specifies the GitHub username.
- `<token>`: (Optional) Specifies your GitHub access token. If omitted, you might encounter rate limits for extensive API requests. Generate a personal access token [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).
- `<extension>`: (Optional) Specifies the file extension to download. By default, the script downloads all files.
- `<filename>`: (Optional) Specifies a string to search within filenames. The script will only download files with names containing this string.
- `<timeframe_created>`: (Optional) Filters gists based on creation date. Accepts `YYYY-MM-DD`, `YYYY-MM`, or `YYYY`.
- `<timeframe_updated>`: (Optional) Filters gists based on update date. Accepts `YYYY-MM-DD`, `YYYY-MM`, or `YYYY`.
- `--overwrite`: (Optional) Controls whether existing files should be overwritten. If this argument is omitted, files with the same name will not be downloaded.

For instance, if you wish to download all '.md' files from 'shaunjohann', created in 2023, and want to overwrite any existing files, you'd execute:

```bash
python3 downloadGists.py shaunjohann --extension .md --timeframe_created 2023 --overwrite
```

## Note on Rate Limits

As it stands, the GitHub API allows 60 requests per hour for unauthenticated requests and 5000 requests per hour for authenticated requests. However, these limits can change, so we recommend verifying the current rate limits at the [GitHub REST API documentation](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting).

## Credits

We owe gratitude to [leoloobeek](https://gist.github.com/leoloobeek) whose groundwork was the inspiration for this script. See the original gist [here](https://gist.github.com/leoloobeek/3be8b835988e8d926a4387019370db8d).

Despite not being a coder, the process of creating this script was both challenging and rewarding. We extend a special thanks to [Cursor](https://cursor.so) and their Chat and Agents features for making this project accessible and comprehensible. We highly recommend their platform for all users, regardless of experience level.

Thank you for being a part of our journey to simplify gist downloads for everyone!
- SJ @ imagined.ai
