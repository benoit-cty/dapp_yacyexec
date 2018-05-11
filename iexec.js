// /opt/yacy_search_server/stopYACY.sh
module.exports = {
  name: 'YacyExec',
  app: {
    type: 'DOCKER',
    envvars: 'XWDOCKERIMAGE=trancept/yacyexec:firsttry',
  },
  work: {
    cmdline: 'http://www.google.com',
  }
};
