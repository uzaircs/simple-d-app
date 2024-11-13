import { getCertificates } from "@/services/transactions";
import { reactive } from "vue";

export const store = reactive({
  isLoading: false,
  transactions: [],
  transactionsPending: false,
  remainingTime: 60,
  getTransactions() {
    getCertificates().then((response) => {
      this.transactions = response.data.reverse().slice(0, 5);
      this.transactionsPending = false;
    });
  },
  issueCertificate() {},
  toggleLoading() {
    this.isLoading = !this.isLoading;
  },
});
