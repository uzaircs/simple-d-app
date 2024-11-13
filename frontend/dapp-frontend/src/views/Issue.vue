<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { issueCertificate, revokeCertificate } from "../services/transactions";
import { store } from "../store/index";
let revoke = {};
const revoking = ref(false);
const revokeC = () => {
  revoking.value = true;
  revokeCertificate(revoke.name, revoke.course, revoke.grade)
    .then((response) => {
      revoking.value = false;
      revoke = {};
      console.log(response);
      alert("Certificate revoked successfully");
    })
    .catch((error) => {
      revoking.value = false;
      console.log(error);
    });
};
const progressBarWidth = computed(() => {
  let width = 60 - store.remainingTime + 1;
  width = (width / 60) * 100;
  return width;
});
const copyText = (text: string) => {
  navigator.clipboard.writeText(text);
  alert("Copied to clipboard");
};
let student: any = {
  name: "",
  course: "",
  grade: "",
};
onMounted(() => {
  store.getTransactions();
});

const issue = () => {
  student.issueDate = new Date().toDateString();
  console.log(student);
  store.toggleLoading();
  issueCertificate(student)
    .then((response) => {
      store.transactionsPending = true;
      alert("Certificate issued successfully");
      window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth",
      });
      student = {};
      let interval = setInterval(() => {
        if (store.remainingTime > 0) {
          store.remainingTime -= 1;
        } else {
          clearInterval(interval);
          store.remainingTime = 60;
        }
      }, 1000);
      setTimeout(() => {
        store.getTransactions();
      }, 60 * 1000);
      store.toggleLoading();
    })
    .catch((error) => {
      console.log(error);
      store.toggleLoading();
    });
};
</script>
<template>
  <div class="row">
    <div class="col-sm-12 col-md-6">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title m-0">Issue a Certificate</h5>
          <div>
            <small
              >Enter details of the student and course to issue a certificate
              for</small
            >
          </div>
          <hr class="mb-2" />
          <div class="row">
            <div class="col-sm-12 col-md-6">
              <div class="form-group">
                <label for="student_name" class="control-label"
                  >Student Name</label
                >
                <input
                  v-model="student.name"
                  placeholder="John Doe"
                  type="text"
                  class="form-control"
                  id="student_name"
                />
              </div>
            </div>
            <div class="col-sm-12 col-md-6">
              <div class="form-group">
                <label for="course_title" class="control-label">Course</label>
                <input
                  v-model="student.course"
                  placeholder="Blockchain & Cryptocurrency"
                  type="text"
                  class="form-control"
                  id="course_title"
                />
              </div>
            </div>
            <div class="col-sm-12 col-md-6">
              <div class="form-group">
                <label for="grade" class="control-label">Grade</label>
                <input
                  v-model="student.grade"
                  type="text"
                  class="form-control"
                  id="grade"
                  placeholder="A - F"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="card-footer">
          <button
            v-on:click="issue()"
            v-if="!store.isLoading"
            class="btn btn-primary"
          >
            Issue Certificate
          </button>
          <button
            disabled="true"
            v-if="store.isLoading"
            class="btn btn-primary"
          >
            <span class="spinner-border spinner-border-sm"></span>
          </button>
        </div>
      </div>
    </div>
    <div class="col-sm-12 col-md-6">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Steps to Issue a Certificate</h5>
          <ol>
            <li>
              Enter the student ID, student name, course title, grade and marks
            </li>
            <li>Click on the Issue Certificate button</li>
            <li>
              Wait for the certificate to be issued.
              <b>It might take couple of second</b> to publish on Blockchain
            </li>
            <li>
              Once the certificate is issued, you will see a success message
            </li>
            <li>
              Go to
              <router-link
                active-class="active"
                aria-current="page"
                to="/verify-certificate"
                >Verify</router-link
              >
              and enter certificate hash to verify certificate
            </li>
          </ol>
          <h5 class="card-title">Verify existing certificate</h5>
          <ol>
            <li>
              Go to
              <router-link
                active-class="active"
                aria-current="page"
                to="/verify-certificate"
                >Verify</router-link
              >
              and enter certificate hash to verify certificate
            </li>
            <li>
              You can choose hash from the table below or enter a random hash to
              view response when certificate does not exists
            </li>
          </ol>
        </div>
      </div>
    </div>
  </div>
  <div class="row mt-4">
    <div class="col-sm-12 col-md-6">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Revoke a Certificate</h5>
          <div class="row align-items-center">
            <div class="col-12">
              <div class="form-group">
                <label for="r_name" class="control-label">Name</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="revoke.name"
                  id="r_name"
                />
              </div>
              <div class="form-group">
                <label for="r_name" class="control-label">Course</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="revoke.course"
                  id="r_name"
                />
              </div>
              <div class="form-group">
                <label for="r_name" class="control-label">Grade</label>
                <input
                  type="text"
                  class="form-control"
                  v-model="revoke.grade"
                  id="r_name"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="card-footer">
          <button
            v-if="!revoking"
            v-on:click="revokeC()"
            class="btn btn-danger"
          >
            Revoke Certificate
          </button>
          <button disabled="true" v-if="revoking" class="btn btn-danger">
            <span class="spinner-border spinner-border-sm"></span>
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="row mt-4 extra-margin">
    <div class="col">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">
            Last 5 Certificates Issued
            <span
              v-if="store.transactionsPending"
              class="spinner-border spinner-border-sm"
            ></span>
            <br v-if="store.transactionsPending" />
            <small class="text-muted" v-if="store.transactionsPending"
              >It may take upto 60 seconds for new transaction to appear
              here...</small
            >
            <br v-if="store.transactionsPending" />
            <small v-if="store.transactionsPending" class="text-muted">
              Please wait... {{ store.remainingTime }}</small
            >
          </h5>
          <div class="progress" v-if="store.transactionsPending">
            <div
              class="progress-bar"
              :style="{ width: progressBarWidth + '%' }"
              role="progressbar"
            ></div>
          </div>
          <div class="table-responsive">
            <table class="table table-hover table-bordered">
              <thead>
                <tr>
                  <th scope="col">Certificate Hash</th>
                  <th scope="col">Student Name</th>
                  <th scope="col">Course</th>
                  <th scope="col">Grade</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in store.transactions">
                  <td>
                    <small class="text-muted">
                      {{ item.cert_hash.substring(0, 20) + "..." }}
                      <a
                        class="text-primary ml-1"
                        target="_blank"
                        :href="`https://sepolia.etherscan.io/tx/${item.tx_hash}`"
                      >
                        View on Etherscan
                        <br />
                      </a>
                      <small>
                        <button
                          class="btn btn-link btn-xs btn-sm"
                          @click="copyText(item.tx_hash)"
                        >
                          Copy transaction hash
                        </button>
                        <button
                          class="btn btn-link btn-xs btn-sm"
                          @click="copyText(item.cert_hash)"
                        >
                          Copy Certificate hash
                        </button>
                      </small>
                    </small>
                  </td>
                  <td>{{ item.name }}</td>
                  <td>
                    {{ item.course }} <br /><small class="text-muted">{{
                      item.teacherName
                    }}</small>
                  </td>
                  <td>{{ item.grade }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
