import http from 'k6/http';
import { check } from 'k6';
import { buildKubernetesBaseUrl, generatePod, getParamsWithAuth, getTestNamespace, randomString } from './util.js';

const baseUrl = buildKubernetesBaseUrl();
const namespace = getTestNamespace();

http.setResponseCallback(http.expectedStatuses(201));

export default function() {
  const podName = 'violating-pod'; // using the specified name
  const pod = generatePod(podName);
  pod.metadata.labels = {
    "environment.tess.io/name": 'staging'
  }

  const params = getParamsWithAuth();
  params.headers['Content-Type'] = 'application/json';

  const createRes = http.post(`${baseUrl}/api/v1/namespaces/${namespace}/pods?dryRun=All`, JSON.stringify(pod), params);
  console.log("received response " + createRes.status + " " + createRes.status_text)
  check(createRes, {
    'verify response code of POST is 201': r => r.status === 201
  });
}

export function teardown() {}

