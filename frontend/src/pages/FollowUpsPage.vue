
<template>
  <q-page class="q-pa-md">
    <!-- Page Header -->
    <div class="row items-center justify-between q-mb-lg">
      <div>
        <div class="text-overline text-grey-7">LEAD MANAGEMENT</div>
        <div class="text-h4 text-weight-bold">Follow-ups</div>
        <div class="text-grey-7 q-mt-xs">
          Manage parent and tutor follow-up activities.
        </div>
      </div>

      <q-btn
        color="primary"
        icon="add"
        label="Schedule Follow-up"
        unelevated
        @click="openCreateDialog"
      />
    </div>

    <!-- Statistics -->
    <div class="row q-col-gutter-md q-mb-lg">
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-grey-7">Total Follow-ups</div>
            <div class="text-h4 text-weight-bold q-mt-sm">
              {{ followUps.length }}
            </div>
            <q-icon name="event_note" color="primary" size="28px" />
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-grey-7">Pending</div>
            <div class="text-h4 text-weight-bold text-orange q-mt-sm">
              {{ countByStatus('Pending') }}
            </div>
            <q-icon name="schedule" color="orange" size="28px" />
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-grey-7">Completed</div>
            <div class="text-h4 text-weight-bold text-positive q-mt-sm">
              {{ countByStatus('Completed') }}
            </div>
            <q-icon name="task_alt" color="positive" size="28px" />
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-grey-7">Missed</div>
            <div class="text-h4 text-weight-bold text-negative q-mt-sm">
              {{ countByStatus('Missed') }}
            </div>
            <q-icon name="event_busy" color="negative" size="28px" />
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Filters -->
    <q-card flat bordered>
      <q-card-section>
        <div class="row q-col-gutter-md items-center">
          <div class="col-12 col-md-5">
            <q-input
              v-model="search"
              outlined
              dense
              clearable
              placeholder="Search lead, parent or tutor..."
            >
              <template #prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>

          <div class="col-12 col-md-3">
            <q-select
              v-model="statusFilter"
              :options="statusOptions"
              outlined
              dense
              emit-value
              map-options
              label="Filter by status"
            />
          </div>

          <div class="col-12 col-md-2">
            <q-select
              v-model="methodFilter"
              :options="methodOptions"
              outlined
              dense
              label="Method"
            />
          </div>

          <div class="col-12 col-md-2">
            <q-btn
              outline
              color="primary"
              icon="refresh"
              label="Refresh"
              class="full-width"
              @click="loadData"
            />
          </div>
        </div>
      </q-card-section>

      <q-separator />

      <!-- Follow-ups Table -->
      <q-table
        :rows="filteredFollowUps"
        :columns="columns"
        row-key="id"
        :loading="loading"
        flat
        :pagination="{ rowsPerPage: 10 }"
        no-data-label="No follow-ups found"
      >
        <template #body-cell-lead="props">
          <q-td :props="props">
            <div class="text-weight-bold">
              {{ getLeadName(props.row.lead_id) }}
            </div>
            <div class="text-caption text-grey-7">
              {{ getLeadCode(props.row.lead_id) }}
            </div>
          </q-td>
        </template>

        <template #body-cell-tutor="props">
          <q-td :props="props">
            {{ getTutorName(props.row.tutor_id) }}
          </q-td>
        </template>

        <template #body-cell-follow_up_at="props">
          <q-td :props="props">
            <div class="text-weight-medium">
              {{ formatDate(props.row.follow_up_at) }}
            </div>
            <div class="text-caption text-grey-7">
              {{ formatTime(props.row.follow_up_at) }}
            </div>
          </q-td>
        </template>

        <template #body-cell-method="props">
          <q-td :props="props">
            {{ props.row.method || '—' }}
          </q-td>
        </template>

        <template #body-cell-status="props">
          <q-td :props="props">
            <q-badge
              :color="statusColor(props.row.status)"
              :label="props.row.status"
              class="q-pa-sm"
            />
          </q-td>
        </template>

        <template #body-cell-actions="props">
          <q-td :props="props">
            <q-btn
              flat
              round
              dense
              color="primary"
              icon="visibility"
              @click="openDetails(props.row)"
            >
              <q-tooltip>View details</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Create Follow-up Dialog -->
    <q-dialog v-model="createDialog" persistent>
      <q-card style="width: 650px; max-width: 95vw">
        <q-card-section class="row items-center">
          <div class="text-h6 text-weight-bold">Schedule Follow-up</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section>
          <q-form @submit.prevent="createFollowUp">
            <div class="row q-col-gutter-md">

              <div class="col-12">
                <q-select
                  v-model="form.lead_id"
                  :options="leadOptions"
                  option-label="label"
                  option-value="value"
                  emit-value
                  map-options
                  outlined
                  label="Select Lead *"
                  :rules="[val => !!val || 'Please select a lead']"
                />
              </div>

              <div class="col-12">
                <q-select
                  v-model="form.tutor_id"
                  :options="tutorOptions"
                  option-label="label"
                  option-value="value"
                  emit-value
                  map-options
                  clearable
                  outlined
                  label="Select Tutor (Optional)"
                />
              </div>

              <div class="col-12 col-sm-6">
                <q-input
                  v-model="form.follow_up_date"
                  outlined
                  type="date"
                  label="Follow-up Date *"
                  :rules="[val => !!val || 'Date is required']"
                />
              </div>

              <div class="col-12 col-sm-6">
                <q-input
                  v-model="form.follow_up_time"
                  outlined
                  type="time"
                  label="Follow-up Time *"
                  :rules="[val => !!val || 'Time is required']"
                />
              </div>

              <div class="col-12 col-sm-6">
                <q-select
                  v-model="form.method"
                  :options="['Call', 'WhatsApp', 'Message', 'Other']"
                  outlined
                  label="Follow-up Method"
                  clearable
                />
              </div>

              <div class="col-12 col-sm-6">
                <q-select
                  v-model="form.status"
                  :options="['Pending', 'Completed', 'Missed', 'Rescheduled']"
                  outlined
                  label="Status"
                />
              </div>

              <div class="col-12">
                <q-input
                  v-model="form.outcome"
                  outlined
                  type="textarea"
                  label="Outcome"
                  placeholder="What happened during the call or message?"
                  rows="2"
                />
              </div>

              <div class="col-12">
                <q-input
                  v-model="form.next_action"
                  outlined
                  type="textarea"
                  label="Next Action"
                  placeholder="e.g. Contact parent after demo"
                  rows="2"
                />
              </div>

              <div class="col-12">
                <q-input
                  v-model="form.next_action_date"
                  outlined
                  type="date"
                  label="Next Action Date (Optional)"
                />
              </div>
            </div>

            <div class="row justify-end q-gutter-sm q-mt-lg">
              <q-btn
                flat
                label="Cancel"
                color="grey-7"
                v-close-popup
              />
              <q-btn
                type="submit"
                color="primary"
                label="Save Follow-up"
                unelevated
                :loading="saving"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Details Dialog -->
    <q-dialog v-model="detailsDialog">
      <q-card style="width: 550px; max-width: 95vw">
        <q-card-section class="row items-center">
          <div class="text-h6 text-weight-bold">Follow-up Details</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section v-if="selectedFollowUp">
          <div class="q-mb-md">
            <div class="text-caption text-grey-7">Lead</div>
            <div class="text-subtitle1 text-weight-bold">
              {{ getLeadName(selectedFollowUp.lead_id) }}
            </div>
            <div class="text-caption text-grey-7">
              {{ getLeadCode(selectedFollowUp.lead_id) }}
            </div>
          </div>

          <q-separator class="q-my-md" />

          <div class="row q-col-gutter-md">
            <div class="col-6">
              <div class="text-caption text-grey-7">Tutor</div>
              <div>{{ getTutorName(selectedFollowUp.tutor_id) }}</div>
            </div>

            <div class="col-6">
              <div class="text-caption text-grey-7">Method</div>
              <div>{{ selectedFollowUp.method || '—' }}</div>
            </div>

            <div class="col-6">
              <div class="text-caption text-grey-7">Date</div>
              <div>{{ formatDate(selectedFollowUp.follow_up_at) }}</div>
            </div>

            <div class="col-6">
              <div class="text-caption text-grey-7">Time</div>
              <div>{{ formatTime(selectedFollowUp.follow_up_at) }}</div>
            </div>

            <div class="col-12">
              <div class="text-caption text-grey-7">Status</div>
              <q-badge
                :color="statusColor(selectedFollowUp.status)"
                :label="selectedFollowUp.status"
                class="q-pa-sm"
              />
            </div>

            <div class="col-12">
              <div class="text-caption text-grey-7">Outcome</div>
              <div>{{ selectedFollowUp.outcome || 'Not recorded' }}</div>
            </div>

            <div class="col-12">
              <div class="text-caption text-grey-7">Next Action</div>
              <div>{{ selectedFollowUp.next_action || 'Not set' }}</div>
            </div>

            <div class="col-12">
              <div class="text-caption text-grey-7">Next Action Date</div>
              <div>
                {{ selectedFollowUp.next_action_at
                  ? formatDate(selectedFollowUp.next_action_at)
                  : 'Not set' }}
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from './../boot/axios'


const followUps = ref([])
const leads = ref([])
const tutors = ref([])

const loading = ref(false)
const saving = ref(false)

const search = ref('')
const statusFilter = ref('All')
const methodFilter = ref('All')

const createDialog = ref(false)
const detailsDialog = ref(false)
const selectedFollowUp = ref(null)

const statusOptions = [
  { label: 'All statuses', value: 'All' },
  { label: 'Pending', value: 'Pending' },
  { label: 'Completed', value: 'Completed' },
  { label: 'Missed', value: 'Missed' },
  { label: 'Rescheduled', value: 'Rescheduled' }
]

const methodOptions = ['All', 'Call', 'WhatsApp', 'Message', 'Other']

const columns = [
  { name: 'lead', label: 'Lead / Parent', field: 'lead_id', align: 'left', sortable: true },
  { name: 'tutor', label: 'Tutor', field: 'tutor_id', align: 'left' },
  { name: 'follow_up_at', label: 'Date & Time', field: 'follow_up_at', align: 'left', sortable: true },
  { name: 'method', label: 'Method', field: 'method', align: 'left' },
  { name: 'status', label: 'Status', field: 'status', align: 'left' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const emptyForm = () => ({
  lead_id: null,
  tutor_id: null,
  follow_up_date: '',
  follow_up_time: '',
  method: 'WhatsApp',
  status: 'Pending',
  outcome: '',
  next_action: '',
  next_action_date: ''
})

const form = ref(emptyForm())

const leadOptions = computed(() =>
  leads.value.map(lead => ({
    label: `${lead.lead_code} - ${lead.parent_name} (${lead.student_class})`,
    value: lead.id
  }))
)

const tutorOptions = computed(() =>
  tutors.value
    .filter(tutor => tutor.is_active)
    .map(tutor => ({
      label: `${tutor.full_name} - ${tutor.phone}`,
      value: tutor.id
    }))
)

const filteredFollowUps = computed(() => {
  const query = search.value.toLowerCase().trim()

  return followUps.value.filter(item => {
    const lead = leads.value.find(l => l.id === item.lead_id)
    const tutor = tutors.value.find(t => t.id === item.tutor_id)

    const searchText = [
      lead?.lead_code,
      lead?.parent_name,
      lead?.parent_phone,
      tutor?.full_name,
      item.outcome,
      item.next_action
    ].join(' ').toLowerCase()

    const matchesSearch = !query || searchText.includes(query)
    const matchesStatus =
      statusFilter.value === 'All' ||
      item.status === statusFilter.value

    const matchesMethod =
      methodFilter.value === 'All' ||
      item.method === methodFilter.value

    return matchesSearch && matchesStatus && matchesMethod
  })
})

function countByStatus(status) {
  return followUps.value.filter(item => item.status === status).length
}

function getLeadName(id) {
  const lead = leads.value.find(item => item.id === id)
  return lead ? lead.parent_name : `Lead #${id}`
}

function getLeadCode(id) {
  const lead = leads.value.find(item => item.id === id)
  return lead?.lead_code || ''
}

function getTutorName(id) {
  if (!id) return 'Not assigned'

  const tutor = tutors.value.find(item => item.id === id)
  return tutor ? tutor.full_name : `Tutor #${id}`
}

function formatDate(value) {
  if (!value) return '—'

  return new Date(value).toLocaleDateString('en-PK', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

function formatTime(value) {
  if (!value) return '—'

  return new Date(value).toLocaleTimeString('en-PK', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  })
}

function statusColor(status) {
  const colors = {
    Pending: 'orange',
    Completed: 'positive',
    Missed: 'negative',
    Rescheduled: 'blue'
  }

  return colors[status] || 'grey'
}

async function loadData() {
  loading.value = true

  try {
    const [followUpRes, leadRes, tutorRes] = await Promise.all([
      api.get('/api/follow-ups/'),
      api.get('/api/leads/'),
      api.get('/api/tutors/')
    ])

    followUps.value = followUpRes.data
    leads.value = leadRes.data
    tutors.value = tutorRes.data
  } catch (error) {
    console.error('Follow-ups loading error:', error)

    window.alert(
      error.response?.data?.detail ||
      'Follow-ups load nahi ho sake. Backend check karein.'
    )
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  form.value = emptyForm()
  createDialog.value = true
}

async function createFollowUp() {
  if (!form.value.lead_id) return

  if (!form.value.follow_up_date || !form.value.follow_up_time) {
    window.alert('Follow-up date aur time select karein.')
    return
  }

  saving.value = true

  try {
    const followUpAt =
      `${form.value.follow_up_date}T${form.value.follow_up_time}:00`

    const nextActionAt = form.value.next_action_date
      ? `${form.value.next_action_date}T09:00:00`
      : null

    const payload = {
      lead_id: form.value.lead_id,
      tutor_id: form.value.tutor_id || null,
      follow_up_at: followUpAt,
      method: form.value.method || null,
      status: form.value.status,
      outcome: form.value.outcome || null,
      next_action: form.value.next_action || null,
      next_action_at: nextActionAt
    }

    await api.post('/api/follow-ups/', payload)

    createDialog.value = false
    await loadData()

    window.alert('Follow-up successfully created.')
  } catch (error) {
    console.error('Follow-up creation error:', error)

    window.alert(
      error.response?.data?.detail ||
      'Follow-up create nahi ho saka.'
    )
  } finally {
    saving.value = false
  }
}

function openDetails(item) {
  selectedFollowUp.value = item
  detailsDialog.value = true
}

onMounted(loadData)
</script>
<style scoped>
.q-page {
    background: aliceblue;
}
</style>
