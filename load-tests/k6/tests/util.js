export const generatePod = (name = 'test', image = 'nginx:latest') => {
  return {
    apiVersion: 'v1',
    kind: 'Pod',
    metadata: {
      name: name,
      namespace: 'load-test',
      labels: {
        "environment.tess.io/name": 'staging'
      }
    },
    spec: {
      containers: [
        {
          name: 'container-with-privileged',
          image: image,
          ports: [
            {
              name: 'nginx-port',
              hostPort: 80,
              containerPort: 80
            }
          ],
          securityContext: {
            privileged: true,
            capabilities: {
              add: [
                "CAP_NET_RAW", "NET_RAW", "NET_BIND_SERVICE", "SETUID", "SETGID", "SYS_ADMIN", "NET_ADMIN", 
                "AUDIT_CONTROL", "AUDIT_READ", "BLOCK_SUSPEND", "BPF", "CHECKPOINT_RESTORE", "DAC_READ_SEARCH", 
                "IPC_LOCK", "IPC_OWNER", "LEASE", "LINUX_IMMUTABLE", "MAC_ADMIN", "MAC_OVERRIDE", "NET_BROADCAST", 
                "PERFMON", "SYS_BOOT", "SYS_MODULE", "SYS_NICE", "SYS_PACCT", "SYS_PTRACE", "SYS_RAWIO", "SYS_RESOURCE", 
                "SYS_TIME", "SYS_TTY_CONFIG", "SYSLOG", "WAKE_ALARM"
              ]
            }
          }
        }
      ],
      hostIPC: true,
      hostPID: true,
      hostNetwork: true,
      securityContext: {
        runAsUser: 0
      },
      volumes: [
        {
          name: 'host-path-volume',
          hostPath: {
            path: '/var/log'
          }
        },
        {
          name: 'host-path-volume-2',
          hostPath: {
            path: '/tmp'
          }
        }
      ],
      hostAliases: [
        {
          ip: "127.0.0.1",
          hostnames: ["localhost"]
        }
      ]
    }
  }
}


export const generateConfigmap = (name = 'test') => {
  return {
    kind: "ConfigMap",
    apiVersion: "v1",
    metadata: {
      name: name
    }
  }
}

export const generateSecret = (name = 'test') => {
  return {
    kind: "Secret",
    apiVersion: "v1",
    metadata: {
      name: name
    }
  }
}

export const buildKubernetesBaseUrl = () => {
  return `https://${__ENV.KUBERNETES_SERVICE_HOST}:${__ENV.KUBERNETES_SERVICE_PORT}`;
}

export const getTestNamespace = () => {
  return __ENV.POD_NAMESPACE;
}

export const getParamsWithAuth = () => {
  return {
    headers: {
      'Authorization': `Bearer ${__ENV.KUBERNETES_TOKEN}`
    }
  }
}

export const randomString = (length) => {
  const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
  const charactersLength = characters.length;
  let result = '';
  let counter = 0;
  while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
  }
  return result;
}
