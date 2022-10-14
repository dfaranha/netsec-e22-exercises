# Exercises: Transport Layer Security

## Preliminaries

We do not require any new dependencies for this exercise. Make sure to have Wireshark and `mitmproxy` installed in your machine.

### Network Layout and Preparation

This time the network will be simpler than the previous one, but will follow the same general layout, depicted below.

As previously, there are two wireless networks (`NETSEC` and `SYSSEC`), and the wired network is on subnetwork `192.168.3.0/24`.
The Access Point (AP) serves as the _router_ between the wireless and the wired network.
The Web server runs on a Raspberry Pi in the wired network, with IP address `192.168.3.2`, and abstracts a machine running on the Internet, to/from which traffic is routed by intermediate nodes.

![image](https://github.com/dfaranha/netsec-e22-exercises/blob/main/06_transport_layer_security/network-layout.png)

Connect to one of the wireless networks using the host system (you know the password) and test that you can connect to `http://192.168.3.2/` using a Web browser (this time we are using the default port `80`).
The traffic between your browser and the server is now being routed by the AP with manually inserted static routes.

Make sure that you can `ping 192.168.3.2` from your machine and access the HTTP address above.
Verify that you can capture traffic between the host and `192.168.3.2` using Wireshark, to confirm that the interface is functional.
Now access `https://192.168.3.2/` (HTTPS) and you will receive a warning about the self-signed certificate, which you should accept as trusted.

## Exercise 1: Malicious-in-the-middle against HTTP

Connect a mobile device to the wireless network and take note of its address `192.168.1/2.X`, referred from here on as `mobile`.
You can typically find the IP address of your mobile device by looking into the network configuration.
In your machine, type `ifconfig` or `ip a` in a terminal and take note of its IP address `192.168.1/2.Z`

**Observation**: If you do not have a mobile device available, ask a colleague to be the client or use the host machine as the victim.

Change the network configuration of your mobile device manually. On Android, this means changing the `IP Settings` to `Static`.
Use the same `192.168.1/2.X` as the IP address, `192.168.1/2.Z` as the Gateway/DNS and `255.255.255.0` as the network mask.

In your machine, let's change the configuration for traffic to be forwarded.

**Observation**: If you are running Mac OS, look at the [official mitmproxy instructions](https://docs.mitmproxy.org/stable/howto-transparent/). If you are running Windows, there is [information online](https://stackoverflow.com/questions/61590951/how-do-i-set-up-transparent-proxy-on-windows-proxy-machine) pointing to a handy [Python script](https://github.com/mitmproxy/mitmproxy/blob/main/mitmproxy/platform/windows.py) that sets up the configuration.

For Linux, the following configurations need to be performed to enable IP forwarding such that your machine can forward IPv4 traffic while avoiding ICMP redirects:

```
$ sudo sysctl -w net.ipv4.ip_forward=1
$ sudo sysctl -w net.ipv4.conf.all.send_redirects=0
```

It might be necessary to also set the following, more specific setting, where `<interface>` is replaced with you network interface (e.g., `wlan0` or `enp5s0`):
```
$ sudo sysctl -w net.ipv4.conf.<interface>.send_redirects=0
```

We will run `mitmproxy` to perform some processing of the captured traffic. First, configure the `iptables` firewall to send all HTTP traffic captured at ports `80` and `443` in your machine to port `8080` under control of `mitmproxy`:

```
$ sudo iptables -A FORWARD --in-interface <interface> -j ACCEPT
$ sudo iptables -t nat -A PREROUTING -i <interface> -p tcp --dport 80 -j REDIRECT --to-port 8080
$ sudo iptables -t nat -A PREROUTING -i <interface> -p tcp --dport 8000 -j REDIRECT --to-port 8080
$ sudo iptables -t nat -A PREROUTING -i <interface> -p tcp --dport 443 -j REDIRECT --to-port 8080
```

Now run `mitmproxy` in _transparent_ mode. Notice that we need it to accept the self-signed certificate from the Web server:

```
$ mitmproxy --ssl-insecure --mode transparent --showhost
```

If everything is working correctly, you should try again to access the Web server `http://192.168.3.2/` in your mobile device and start seeing captured _flows_ in the `mitmproxy` window.
In this window, you can select a flow by using the arrows and pressing ENTER, while pressing the letter `q` goes back to the overview screen.

**Observation**: If you **cannot** see flows in `mitmproxy`, try restoring your `IP Settings` configuration to DHCP and configure ``192.168.1/2.Z`` as the `Proxy` running on port `8080`. Replace the command line above to run `mitmproxy` in _proxy_ mode:

```
$ mitmproxy --ssl-insecure --showhost
```
Access the Login page, enter some credentials and observe that they are visible in `mitmproxy` as part of an `HTTP POST` method.

## Exercise 2: Malicious-in-the-middle against HTTPS

Now try accessing `https://192.168.3.2/` in your mobile device.
You should get another warning about a non-trusted certificate! Inspect the certificate and check that it is suspicious indeed. :)
After accepting the new certificate, you should be able to access the website normally.
Make sure you access the Login page again and that captured credentials are still visible.

## BONUS: Manipulate traffic in mitmproxy

If you reached this point, we have a bonus round for you.
Let's use the scripting capability of `mitmproxy` to mount an _active_ attack.
You have seen that our simple website has a login capability, for which the _right_ credentials are not known. There should be legitimate traffic in the local network of successful login attempts, so find the correct flows in `mitmproxy` to obtain a pair of correct credentials.

Now access the website through your mobile device with the right credentials and login. You should now be able to access the `View Secrets` and `Upload Secrets` functionalities.
The `View Secrets` functionality will just show you some secret keyword, which should be visible in `mitmproxy` as well.
The `Upload Secrets` functionality is more interesting and allows the user to encrypt a message under a public key returned by the server.
Your final task is to _replace_ that public key with a key pair for which you know the private key (to be able to decrypt).
The code for the server portion is provided for reference in the repository inside the folder `simple-website`.

In order to achieve your goal, generate an RSA key pair in PEM format and plug the values marked as TODO in the file `simple-website/mitm_pk.py`. Now restart `mitmproxy` with the command below:

```
$ mitmproxy --mode transparent --showhost -s mitm_pk.py
```

Recover the message from the encryption provided by the client.
