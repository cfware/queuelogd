# @cfware/queuelogd

[![MIT][license-image]](LICENSE)

CFWare Queue Logger Daemon

## Building @cfware/queuelogd

Since NPM doesn't install systemd unit files and other system configuration files
I do not plan on publishing this to NPM.

To build a Fedora style RPM:
```sh
npm pack
rpmbuild -ta *.tgz
```

## Running tests

No automated tests are provided by this repository, see [@cfware/queue_log-mysql]
for tests.

[license-image]: https://img.shields.io/github/license/cfware/queuelogd.svg
[@cfware/queue_log-mysql]: https://github.com/cfware/queue_log-mysql
