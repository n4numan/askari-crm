
<template>
  <q-layout view="hHh Lpr lFf" class="bg-grey-1">

    <!-- TOP HEADER -->
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>

        <q-btn
          flat
          round
          dense
          icon="menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title class="text-weight-bold">
          Askari Academy CRM
          <q-badge color="secondary" text-color="dark" class="q-ml-sm">
            v1.0
          </q-badge>
        </q-toolbar-title>

        <!-- DESKTOP SEARCH -->
        <q-input
          v-if="!$q.screen.lt.md"
          v-model="searchQuery"
          dense
          outlined
          dark
          placeholder="Search..."
          class="header-search q-mr-md"
        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>

        <!-- USER ROLE -->
        <q-chip color="secondary" text-color="dark" dense>
          <q-icon name="person" class="q-mr-xs" />
          {{ userRole }}
        </q-chip>

        <!-- LOGOUT -->
        <q-btn
          flat
          round
          dense
          icon="logout"
          color="white"
          @click="logout"
        >
          <q-tooltip>Logout</q-tooltip>
        </q-btn>

      </q-toolbar>

      <!-- MOBILE SEARCH -->
      <q-toolbar v-if="$q.screen.lt.md && showMobileSearch">
        <q-input
          v-model="searchQuery"
          dense
          filled
          dark
          placeholder="Search..."
          class="full-width"
        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>
      </q-toolbar>

    </q-header>

    <!-- LEFT SIDEBAR -->
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      :width="255"
      :breakpoint="1024"
      class="bg-white"
    >

      <div class="column fit">

        <!-- SIDEBAR BRAND -->
        <div class="q-pa-md row items-center">
          <q-avatar color="primary" text-color="white" size="45px">
            <span class="text-weight-bold">AA</span>
          </q-avatar>

          <div class="q-ml-sm">
            <div class="text-weight-bold text-primary">
              Askari Academy
            </div>
            <div class="text-caption text-grey-7">
              Lead Management System
            </div>
          </div>
        </div>

        <q-separator />

        <!-- MENU -->
        <q-scroll-area class="col">

          <q-list padding>

            <q-item-label header class="text-grey-7">
              WORKSPACE
            </q-item-label>

            <q-item
              v-for="item in menuItems"
              :key="item.title"
              clickable
              v-ripple
              :to="item.path"
              exact
              active-class="active-menu"
              class="q-mx-sm rounded-borders"
            >
              <q-item-section avatar>
                <q-icon :name="item.icon" />
              </q-item-section>

              <q-item-section>
                {{ item.title }}
              </q-item-section>
            </q-item>

            <q-separator class="q-my-md" />

            <q-item-label header class="text-grey-7">
              ACCOUNT
            </q-item-label>

            <q-item
              clickable
              v-ripple
              to="/settings"
              active-class="active-menu"
              class="q-mx-sm rounded-borders"
            >
              <q-item-section avatar>
                <q-icon name="settings" />
              </q-item-section>

              <q-item-section>
                Settings
              </q-item-section>
            </q-item>

          </q-list>

        </q-scroll-area>

        <!-- SIDEBAR FOOTER -->
        <q-separator />

        <div class="q-pa-md">
          <div class="row items-center">
            <q-avatar color="blue-1" text-color="primary" icon="admin_panel_settings" />

            <div class="q-ml-sm">
              <div class="text-weight-medium">Academy Team</div>
              <div class="text-caption text-grey-7">
                {{ userRole }}
              </div>
            </div>
          </div>
        </div>

      </div>

    </q-drawer>

    <!-- MAIN PAGE -->
    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'

const $q = useQuasar()
const router = useRouter()

const leftDrawerOpen = ref(false)
const showMobileSearch = ref(false)
const searchQuery = ref('')

const userRole = computed(() => {
  return localStorage.getItem('role') || 'Admin'
})

// SIDEBAR MENU
const menuItems = [
  {
    title: 'Dashboard',
    icon: 'dashboard',
    path: '/'
  },
  {
    title: 'All Leads',
    icon: 'groups',
    path: '/leads'
  },
  {
    title: 'Tutors',
    icon: 'school',
    path: '/tutors'
  },
  {
    title: 'Demo Calendar',
    icon: 'event',
    path: '/demos'
  },
  {
    title: 'Follow-ups',
    icon: 'phone_callback',
    path: '/follow-ups'
  },
  {
    title: 'Tuitions',
    icon: 'menu_book',
    path: '/tuitions'
  },
  // {
  //   title: 'Reports',
  //   icon: 'analytics',
  //   path: '/reports'
  // }
]

// LOGOUT
function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('role')

  $q.notify({
    type: 'positive',
    message: 'Logged out successfully',
    position: 'top'
  })

  // Login route will be added when authentication is implemented.
  router.push('/')
}
</script>

<style scoped>
.header-search {
  width: 220px;
}

.active-menu {
  background: #e8edfa;
  color: #172554;
  font-weight: 600;
  border-left: 3px solid #d4a72c;
}

.q-drawer {
  border-right: 1px solid #e5e7eb;
}
</style>
