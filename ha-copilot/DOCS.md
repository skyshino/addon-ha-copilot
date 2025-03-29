# ha-copilot addon: improve the HA configuration efficiency

This addon include several web pages, each of page provide a way to configure HA. It is designed to improve the efficiency of configuring HA.

At this version, the tool only include the following pages:

- Device properity edit pages: change the area and label of device.
- YAML Edit pages: edit automation YAML script.

# How to use

This addon include several web pages, each of page provide a way to configure HA. It is designed to improve the efficiency of configuring HA.

At this version, the tool only include the following pages:

- Device properity edit pages

  In this tab page, you can change the area and label of device.
  - The Aera Property Edit tab:
    
    You can move several device into or out of a Aera.
  - The Label Property Edit tab:

    You can move several device into or out of a Label.
- YAML Edit pages:

  In this tab page, you can edit the YAML script of automation.

  <span style="color:red">**Note**</span>: _Be caution with this, it will chage the automations.xml of the HA. This may broke other automations._  

# Installation

The installation of this add-on is pretty straightforward and not different in
comparison to installing any other Home Assistant add-on.

1. Click the Home Assistant My button below to add the repository to your Home
   Assistant instance's addon shop.

    [![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgitee.com%2Fskyshino%2Faddon-ha-copilot)

2. Find the "ha-copilot" add-on in the Home Assistant add-on store and click it.
3. Click the "Install" button to install the add-on.
4. Start the "Example" add-on.
5. Check the logs of the "Example" add-on to see it in action.

## Configuration

Now the addon support to configure the log level.

**Note**: _Remember to restart the add-on when the configuration is changed._

Configuration:

```yaml
log_level: info
```

### Option: `log_level`

The `log_level` option controls the level of log output by the add-on and can
be changed to be more or less verbose, which might be useful when you are
dealing with an unknown issue. Possible values are:

- `trace`: Show every detail, like all called internal functions.
- `debug`: Shows detailed debug information.
- `info`: Normal (usually) interesting events.
- `warning`: Exceptional occurrences that are not errors.
- `error`: Runtime errors that do not require immediate action.
- `fatal`: Something went terribly wrong. Add-on becomes unusable.

Please note that each level automatically includes log messages from a
more severe level, e.g., `debug` also shows `info` messages. By default,
the `log_level` is set to `info`, which is the recommended setting unless
you are troubleshooting.

## Changelog & Releases

This repository keeps a change log using [GitHub's releases][releases]
functionality.

Releases are based on [Semantic Versioning][semver], and use the format
of `MAJOR.MINOR.PATCH`. In a nutshell, the version will be incremented
based on the following:

- `MAJOR`: Incompatible or major changes.
- `MINOR`: Backwards-compatible new features and enhancements.
- `PATCH`: Backwards-compatible bugfixes and package updates.

## Support

Got questions?

You have several options to get them answered:

- The Home Assistant [Community Forum][forum].
- [open an issue here][issue] GitHub.

## Authors & contributors

The original setup of this repository is by [skyshino][skyshino].

For a full list of all authors and contributors,
check [the contributor's page][contributors].

## License

MIT License

Copyright (c) 2025-2035 skyshino

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[addon-badge]: https://my.home-assistant.io/badges/supervisor_addon.svg
[addon_github]: https://my.home-assistant.io/redirect/supervisor_addon/?addon=ha-copilot&repository_url=https%3A%2F%2Fgithub.com%2Fskyshino%2Fha_copilot
[addon_gitee]: https://my.home-assistant.io/redirect/supervisor_addon/?repository_url=https%3A%2F%2Fgitee.com%2Fskyshino%2Fha-copilot&addon=ha-copilot
[forum]: https://community.home-assistant.io/t/ha-copilot-addon/869506
[skyshino]: https://github.com/skyshino
[contributors]: https://github.com/skyshino/ha_copilot/issues
[issue]: https://github.com/skyshino/ha_copilot/issues
[releases]: https://github.com/skyshino/ha_copilot/releases
[semver]: http://semver.org/spec/v2.0.0.html
