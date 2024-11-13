<script setup lang="ts">
import { verifyCertificate } from "@/services/transactions";
import { ref } from "vue";
let name = "";
let course = "";
let grade = "";
const verifying = ref(false);
const verification_result = ref(null);
let error = false;
const verify = () => {
  verifying.value = true;
  verifyCertificate(name, course, grade)
    .then((response) => {
      verifying.value = false;
      verification_result.value = response.data;
      console.log(verification_result);
    })
    .catch((error) => {
      verifying.value = false;
      verification_result.value = false;
    });
};
</script>
<template>
  <div class="row">
    <div class="col-sm-12 col-md-6">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Verify a certificate</h5>
          <div class="form-group">
            <label for="name" class="control-label">Name</label>
            <input
              placeholder="Name"
              type="text"
              class="form-control"
              id="name"
              v-model="name"
            />
          </div>
          <div class="form-group">
            <label for="course" class="control-label">Course</label>
            <input
              placeholder="Some course..."
              type="text"
              class="form-control"
              id="course"
              v-model="course"
            />
          </div>
          <div class="form-group">
            <label for="grade" class="control-label">Grade</label>
            <input
              placeholder="A - F"
              type="text"
              class="form-control"
              id="grade"
              v-model="grade"
            />
          </div>
        </div>
        <div class="card-footer">
          <button
            v-if="!verifying"
            class="btn btn-primary"
            v-on:click="verify()"
          >
            Verify
          </button>
          <button v-else class="btn btn-primary" disabled>Verifying...</button>
        </div>
      </div>
    </div>
    <div class="col-sm-12 col-md-6">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Verification Result</h5>
          <div
            v-if="
              (!verification_result || !verification_result.result) &&
              verification_result !== false
            "
          >
            Verification result will appear here...
          </div>
          <div
            v-if="
              verification_result &&
              verification_result.result == 'Certificate is valid.'
            "
          >
            <h4 class="text-success">Certificate is valid</h4>
          </div>
          <div
            v-if="
              verification_result &&
              verification_result.result == 'Certificate does not exist.'
            "
          >
            <h4 class="text-danger">Certificate does not exist!</h4>
          </div>
          <div
            v-if="
              verification_result &&
              verification_result.result == 'Certificate is revoked.'
            "
          >
            <h4 class="text-warning">Certificate has been revoked</h4>
          </div>

          <div v-if="verification_result === false">
            <h4 class="text-danger">
              Certificate does not exist or has been revoked.
            </h4>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
