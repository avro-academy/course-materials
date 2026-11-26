THE NETWORK LAB
Avro Academy · Networking Fundamentals: How the Internet Works

A small, pretend café network that runs inside Docker on your own computer.
Nothing in it can reach your real network or the internet.

  Machine   Network                  Address                        Job
  pc1, pc2  Office  192.168.10.0/24  192.168.10.21, .22             Staff computers
  router    Both                     192.168.10.254 and 10.0.20.254 Joins the two networks
  dns       Servers 10.0.20.0/24     10.0.20.53                     Names like web.cafe.lan
  web       Servers                  10.0.20.80                     The staff intranet website

YOU NEED
  Docker Desktop (docker.com/products/docker-desktop), free for personal use and learning.

USE IT (in a terminal, in this folder)
  docker compose up -d --build     start the lab (the first time takes a minute or two)
  docker compose exec pc1 sh       get onto pc1; type exit to leave
  docker compose down              stop the lab when you're finished
  docker compose up -d             start it again, fresh

MODULE 6: PLANT A FAULT (gateway, dns, firewall or server)
  Mac and Linux:        LAB_FAULT=gateway docker compose up -d --force-recreate
  Windows PowerShell:   $env:LAB_FAULT="gateway"; docker compose up -d --force-recreate
  Clear it (Windows):   $env:LAB_FAULT=""

  Try not to read lab.sh before you've found the fault: it gives the answers away!

FILES
  compose.yaml   the five machines and the "wire" that joins them
  Dockerfile     the small Linux machine they all use (Alpine Linux and network tools)
  lab.sh         gives each machine its address, gateway and job when it starts
  dnsmasq.conf   the names the DNS server knows
  www/           the intranet website
