import api from "./api";
export const getTransactions = async () => {
  return await api.get("/get_transactions");
};
export const issueCertificate = async (data) => {
  return await api.post("/issue", { details: data });
};
export const getCertificates = async () => {
  return await api.get("/issued_certificates");
};
export const verifyCertificate = async (name, course, grade) => {
  return await api.get(`/verify?name=${name}&course=${course}&grade=${grade}`);
};
export const revokeCertificate = async (name, course, grade) => {
  return await api.post(`/revoke?name=${name}&course=${course}&grade=${grade}`);
};
