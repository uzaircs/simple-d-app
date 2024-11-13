<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-white">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">CertiBlock</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link active-class="active" class="nav-link" aria-current="page"
                            to="/issue-certificate">Issue</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link active-class="active" class="nav-link " aria-current="page" to="/verify-certificate">Verify</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link active-class="active" class="nav-link " aria-current="page" to="/about">Project
                            Details</router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>