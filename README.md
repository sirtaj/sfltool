
SFLtool -- SFLphone CLI
=======================

Simple command line interface to SFLphone SIP client, using the DBus
interface.

NOTE: This is currently a very trivial implementation with no real
error checking.


## Implemented Commands

 * `dial <number> [<account alias>]` -- dial the number directly. If no
account alias is specified, the last used account is reused for the call.
 * `callback` -- call back the last person in the call history, whether
 incoming, outgoing or a missed call.
 * `hangup` -- hangup all ongoing calls.
