# ORCIDWorks

<img src="https://orcidhub.org.nz/static/images/logo.png" align="right" width="48" height="48" alt="ORCID Hub logo">

> Collect works metadata from ORCID.org

Adapted from [a gist](https://gist.github.com/Jason-Gush/bcbab1c3c55e5684251ad3b8ee04eded) by [@JasonGush](https://github.com/Jason-Gush), this is a Python script that collects works on ORCID from their API from a list of users affiliated with an institution on the [NZ ORCID Hub](https://orcidhub.org.nz) and outputs them to a CSV file.

## Installation

### Prerequisites

You'll need Python 3.6+ (and [pip](https://pip.pypa.io/en/stable/)).

### API Keys

You'll need to obtain credentials from both the [ORCID.org API](https://info.orcid.org/documentation/features/public-api/) and the [NZ ORCID Hub API](https://orcidhub.org.nz/api-docs). For the latter, choose "Hub API Registration" from the "Settings" menu.

> ℹ We suggest using [the ORCID.org sandbox](https://sandbox.orcid.org/signin) and [Test Hub](https://test.orcidhub.org.nz) first. (See "Configuration" below.)

## Running

Install dependencies:

```shell
pip install -r requirements.txt
```

### Secrets

Rename [`.env.sample`](.env.sample) to `.env`, and copy and paste your access keys and secrets into it at the appropriate lines. (`.env` is included in [`.gitignore`](https://git-scm.com/docs/gitignore), so it won't be committed.)

### Get token

Run [getORCIDToken.py](getORCIDToken.py) to acquire a token. This will log to `getORCIDtoken.log`.

### Run

You should now be able to run the main script, `getworks.py`. (In VSCode, press <kbd>F5</kbd>.) 

## Configuration

Set `testing` to `True` in [getworks.py](https://github.com/AMCollectionsData/ORCIDWorks/blob/4a862b19f71dc44929c532e0acd6f5f4cf535f2c/getworks.py#L20) to have the script use the [ORCID.org sandbox](https://sandbox.orcid.org) and [test.orcidhub.org.nz](https://test.orcidhub.org.nz).

## Libraries

The script uses [python-decouple](https://pypi.org/project/python-decouple/) to maintain separation of settings (API keys and secrets) from code, in `.env`.

## Licensing

Issued under the [MIT](/LICENSE) license.

## Help

Please use [Discussions](//github.com/AMCollectionsData/ORCIDWorks/discussions) to ask for help, or [raise an issue](//github.com/AMCollectionsData/ORCIDWorks/issues/new/choose) to report a bug or request a new feature.

## Contributions

![Alt](https://repobeats.axiom.co/api/embed/ad3754e08280c0c99d0a3f5cdb8b719a1993e495.svg "Repobeats analytics image")
