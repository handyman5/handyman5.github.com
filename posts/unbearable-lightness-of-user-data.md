<!--
.. title: The Unbearable Lightness of User-Data
.. slug: unbearable-lightness-of-user-data
.. date: 2012-10-02 12:00:00 UTC-07:00
.. tags: openstack, til
.. category: 
.. link: 
.. description: 
.. type: text
-->

_(originally from <https://web.archive.org/web/20150423071705/http://ajcsystems.com/blog/blog/2012/10/02/the-unbearable-lightness-of-user-data/>)_

When you launch an instance in OpenStack, it has a big empty box called “User Data”:

![image](/images/png_JtasHKS3b.png)

I never knew what that box was for until today.

### How it’s provided

If an image is configured to use [cloud-init](https://help.ubuntu.com/community/CloudInit), when it starts up it will `curl` a special path:

``` shell
$ curl http://169.254.169.254/2009-04-04/user-data/
```

Since this is a link-local “I don’t have a DHCP address yet” IP, it will work even before networking is configured. The output from this URL is whatever you put in “User Data”.

### How it’s used

cloud-init has a bunch of different tweaks it can apply as an instance launches; it can run `apt-get upgrade`, import ssh keys, disable sshd PasswordAuthentication, run arbitrary commands, and much more. [This sample config](https://web.archive.org/web/20150423071705/http://xebia-france.googlecode.com/svn/training/xebia-spring-travel/trunk/xebia-spring-travel-amazon-aws/src/main/scripts/cloud-config-sample.txt) will give you a pretty good idea about the full capabilities of cloud-init.

### Basic example

When you launch an instance, put the following in “User Data”:

``` shell
#cloud-config
ssh_pwauth: True
```

This will make cloud-init enable PasswordAuthentication in sshd (which it otherwise disables by default), so that you don’t need to use a key to log in to the instance.
