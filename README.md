# drmosh

*Because you know better than the machine*

This is a helper for [`mosh`, the mobile shell](https://mosh.org/),
that replaces its server address detection method. Some weird network
conditions may prevent vanilla `mosh` from working, and `drmosh` may
help you.

## When should you use `drmosh`?

`drmosh` may help you get your Mosh going, if all three points below
apply to your situation:

1. Your SSH connection to the server requires ProxyCommand, or does not
directly connect to the server's IP address;

2. Your SSH connection, when it eventually reaches the server, does not
come through the interface your Mosh client needs to use, and therefore
the local address seen by the SSH server is not correct for the client;

3. On the server, either the local IPv4 address that has the default
route is the correct one for the client, or the correct address never
change and can be hard-coded.

Again, if all three points apply, `drmosh` may be useful for you.

If only 1 applies and 2 doesn't, just run vanilla Mosh with
`--bind-server=any`.
If only 2 applies and 1 doesn't, run Mosh with
`--experimental-remote-ip=remote` or possibly
`--experimental-remote-ip=local`.
Both these scenarios should be easy for plain old Mosh to handle.

If 3 does not apply, then unfortunately `drmosh` cannot help you. In
particular, we can't help you if the server is stuck behind some kind
of NAT and cannot forward ports.

So, here are some scenarios where all three conditions may be
satisfied:

* You use some kind of tunneling tool for the SSH connection, where one
end of the tunnel runs on the client machine and the other end runs on
the server, such as `stunnel`, `kcptun`, `obfs4proxy`, etc.

* SSH's TCP connection and Mosh's UDP connection goes through completely
different paths, for example, SSH has to go through a VPN, but Mosh goes
through the open Internet.

## How to use `drmosh`?

### System Requirements

`drmosh` requires Python 3.5 or above, and of course Mosh. It has
no other dependencies.

### Install

* Download dr-mosh-server.py to the server
* Optionally, edit the config section at the top of the file
* Put it somewhere and make sure it's executable

### Usage

On the client, run `mosh` with some additional arguments:

    mosh --server='path/to/dr-mosh-server.py' --experimental-remote-ip=remote [user@]host

If all goes well, you should have a working remote shell.