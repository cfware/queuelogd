#!/usr/bin/env node

'use strict';

const sd = require('systemd-daemon');
const queuelogd = require('@cfware/queue_log-mysql');

/* Should use a proper config loader.  Good enough example. */
const settings = require(process.argv[2] || '/etc/cfware-queuelogd.json');
const server = new queuelogd(settings);

function shutdown() {
	sd.notify('STOPPING=1');
	server.stop();
}

server.on('listening', () => {
	sd.notify('READY=1');
	sd.watchdog.start();

	process.on('SIGINT', shutdown);
	process.on('SIGTERM', shutdown);
});
server.on('insert-failure', info => {
	/* Should write these to a file that can be parsed/imported some other
	 * time.  Probably should to be CSV encoded. */
	console.log(JSON.stringify(server.columns.map(name => info.data[name])));
});
server.on('shutdown-complete', () => sd.watchdog.stop());
server.start(sd.socket() || settings.listen);
