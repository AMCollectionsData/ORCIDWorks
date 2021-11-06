# ORCIDWorks
> Collect works metadata from ORCID.org

<span style="display:block;text-align:right"><img src="https://orcidhub.org.nz/static/images/logo.png"  width="48" height="48" alt="ORCID Hub logo"></span>

Adapted from [a gist](https://gist.github.com/Jason-Gush/bcbab1c3c55e5684251ad3b8ee04eded) by [@JasonGush](https://github.com/Jason-Gush), this is a Python script that collects works on ORCID from their API from a list of users affiliated with an institution on the [NZ ORCID Hub](https://orcidhub.org.nz).

## Installation

### Prerequisites

You'll need Python 3.6+ (and [pip](https://pip.pypa.io/en/stable/)).

### API Keys

You'll need to obtain credentials from both the [ORCID.org API](https://info.orcid.org/documentation/features/public-api/) and the [NZ ORCID Hub API](https://orcidhub.org.nz/api-docs). For the latter, choose "Hub API Registration" from the "Settings" menu.

> **_NB:_** We suggest using [the ORCID.org sandbox](https://sandbox.orcid.org/signin) and [Test Hub](https://test.orcidhub.org.nz) first. (See [#Configuration](#configuration) below.)

## Running

Install dependencies:

```shell
pip install -r requirements.txt
```

### Secrets
Rename [`.env.sample`](.env.sample) to `.env`, and copy and paste your access keys and secrets into it at the appropriate lines. (`.env` is included in `.gitignore`, so it won't be committed.)


### Run

You should now be able to run the script. In VSCode, press <kbd>F5</kbd>.
## [Configuration](#Configuration)

Set `testing` to `True` in [ORCIDWorks.py](ORCIDWorks.py) to use the [ORCID.org sandbox](https://sandbox.orcid.org) and [test.orcidhub.org.nz](https://test.orcidhub.org.nz).

## Libraries

The script uses [python-decouple](https://pypi.org/project/python-decouple/) to maintain separation of settings (API keys and secrets) from code, in `.env`.

## Licensing

[MIT](/LICENSE).