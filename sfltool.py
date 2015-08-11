#!/usr/bin/env python

__doc__ = '''\
Simple command line interface for SFLphone using DBus interface.
'''

import dbus

service = 'org.sflphone.SFLphone'
object_ns = '/org/sflphone/SFLphone'


class NoSuchAccountError(Exception):
    pass


session_bus = dbus.SessionBus()
config_obj = session_bus.get_object(service, object_ns+'/ConfigurationManager')
config = dbus.Interface(config_obj, service+'.ConfigurationManager')
call_obj = session_bus.get_object(service, object_ns+'/CallManager')
calls = dbus.Interface(call_obj, service+'.CallManager')

QUIET = False

# command name -> command_func
commands = {}

def cmd(name):
    def deco(fn):
        commands[name] = fn
        return fn
    return deco


@cmd('dial')
def dial_number(number, account_alias=None):
    '''Call number, with account with alias if specified, last used otherwise.
    '''
    if account_alias:
        account_id = get_account_by_alias(account_alias)
    else:
        account_id = get_last_used_account()

    if not QUIET:
        print "Calling:", number

    calls.placeCall(account_id, get_unused_call_id(), number)


@cmd('callback')
def repeat_last_call():
    history = config.getHistory()
    old_call = history[0]

    if not QUIET:
        print "Calling:", old_call['peer_number']

    print calls.placeCall(old_call['accountid'],
                    get_unused_call_id(),
                    old_call['peer_number'])


@cmd('hangup')
def hangup_all_calls():
    for call_id in calls.getCallList():
        calls.hangUp(call_id)


# - util -


def get_account_by_alias(account_alias):
    accounts = dict((config.getAccountDetails(acc_id)['Account.alias'], acc_id)
                    for acc_id in config.getAccountList())
    try:
        account_id = accounts[account_alias]
    except KeyError:
        raise NoSuchAccountError(account_alias)

    return account_id


def get_last_used_account():
    return config.getHistory()[0]['accountid']


def get_unused_call_id():
    return str(len(calls.getCallList())+1)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        cmds = ', '.join(sorted(commands.keys()))
        print "%s: commands: %s" % (sys.argv[0], cmds)
        exit(-1)

    commands[sys.argv[1]](*sys.argv[2:])
    exit(0)
