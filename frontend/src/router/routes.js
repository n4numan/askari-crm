
const routes = [
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('@/pages/IndexPage.vue') },

      { path: 'leads', component: () => import('@/pages/LeadsPage.vue') },
      { path: 'tutors', component: () => import('@/pages/TutorsPage.vue') },
      { path: 'demos', component: () => import('@/pages/DemosPage.vue') },
      { path: 'follow-ups', component: () => import('@/pages/FollowUpsPage.vue') },
      { path: 'tuitions', component: () => import('@/pages/TuitionsPage.vue') },
      // { path: 'reports', component: () => import('@/pages/ReportsPage.vue') },
      // { path: 'settings', component: () => import('@/pages/SettingsPage.vue') }
    ],
  },

  // Always leave this as last one
  {
    path: '/:catchAll(.*)*',
    component: () => import('@/pages/ErrorNotFound.vue'),
  }
]

export default routes
