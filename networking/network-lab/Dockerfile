# One small Linux machine, used for every computer in the lab.
FROM alpine:3.22
RUN apk add --no-cache iproute2 iputils traceroute curl bind-tools iptables dnsmasq busybox-extras
ENV ENV=/etc/profile
COPY lab.sh /lab.sh
COPY dnsmasq.conf /etc/dnsmasq.conf
COPY www /www
RUN chmod +x /lab.sh
CMD ["/lab.sh"]
