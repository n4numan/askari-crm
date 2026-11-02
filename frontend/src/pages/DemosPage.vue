
<template>
  <q-page class="q-pa-md q-pa-md-md">
    <!-- Header -->
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h4 text-weight-bold">Demos</div>
      </div>

      <q-btn
        color="primary"
        icon="event"
        label="Schedule Demo"
        unelevated
        @click="openCreateDialog"
      />
    </div>

    <!-- Statistics -->
    <div class="row q-col-gutter-md q-mb-md">
      <div class="col-6 col-md-3">
        <q-card flat bordered class="stat-card">
          <q-card-section>
            <div class="text-grey-7 text-caption">Total Demos</div>
            <div class="text-h4 text-weight-bold">{{ demos.length }}</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-6 col-md-3">
        <q-card flat bordered class="stat-card">
          <q-card-section>
            <div class="text-grey-7 text-caption">Scheduled</div>
            <div class="text-h4 text-weight-bold text-primary">
              {{ countStatus('Scheduled') }}
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-6 col-md-3">
        <q-card flat bordered class="stat-card">
          <q-card-section>
            <div class="text-grey-7 text-caption">Demo Done</div>
            <div class="text-h4 text-weight-bold text-positive">
              {{ countStatus('Demo Done') }}
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-6 col-md-3">
        <q-card flat bordered class="stat-card">
          <q-card-section>
            <div class="text-grey-7 text-caption">Rescheduled</div>
            <div class="text-h4 text-weight-bold text-warning">
              {{ countStatus('Rescheduled') }}
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Confirmation Summary -->
    <div class="row q-col-gutter-md q-mb-md">
      <div class="col-12 col-md-6">
        <q-card flat bordered>
          <q-card-section class="row items-center">
            <q-avatar color="blue-1" text-color="primary" icon="person" />
            <div class="q-ml-md">
              <div class="text-caption text-grey-7">Parent Confirmations</div>
              <div class="text-h6 text-weight-bold">
                {{ demos.filter(d => d.parent_confirmed).length }} /
                {{ demos.length }}
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-6">
        <q-card flat bordered>
          <q-card-section class="row items-center">
            <q-avatar color="green-1" text-color="positive" icon="school" />
            <div class="q-ml-md">
              <div class="text-caption text-grey-7">Tutor Confirmations</div>
              <div class="text-h6 text-weight-bold">
                {{ demos.filter(d => d.tutor_confirmed).length }} /
                {{ demos.length }}
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Filters -->
    <q-card flat bordered>
      <q-card-section>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-7">
            <q-input
              v-model="search"
              outlined
              dense
              clearable
              placeholder="Search lead, tutor, phone or location..."
            >
              <template #prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>

          <div class="col-12 col-md-5">
            <q-select
              v-model="statusFilter"
              :options="statusOptions"
              outlined
              dense
              label="Filter by status"
            />
          </div>
        </div>
      </q-card-section>

      <q-separator />

      <!-- Loading -->
      <div v-if="loading" class="q-pa-xl text-center">
        <q-spinner-dots color="primary" size="40px" />
        <div class="text-grey-7 q-mt-sm">Loading demos...</div>
      </div>

      <!-- Table -->
      <div v-else-if="filteredDemos.length" class="q-pa-sm">
        <q-table
          :rows="filteredDemos"
          :columns="columns"
          row-key="id"
          flat
          :pagination="{ rowsPerPage: 10 }"
          :rows-per-page-options="[10, 20, 50]"
          wrap-cells
        >
          <template #body-cell-lead="props">
            <q-td :props="props">
              <div class="text-weight-bold">
                {{ getLead(props.row.lead_id)?.parent_name || 'Unknown Lead' }}
              </div>
              <div class="text-caption text-grey-7">
                {{ getLead(props.row.lead_id)?.student_class || '' }}
              </div>
              <div class="text-caption text-grey-7">
                {{ getLead(props.row.lead_id)?.parent_phone || '' }}
              </div>
            </q-td>
          </template>

          <template #body-cell-tutor="props">
            <q-td :props="props">
              {{ getTutor(props.row.tutor_id)?.full_name || 'Not assigned' }}
            </q-td>
          </template>

          <template #body-cell-date="props">
            <q-td :props="props">
              <div class="text-weight-medium">
                {{ formatDate(props.row.demo_date) }}
              </div>
              <div class="text-caption text-grey-7">
                {{ formatTime(props.row.demo_time) }}
              </div>
            </q-td>
          </template>

          <template #body-cell-status="props">
            <q-td :props="props">
              <q-badge
                :color="statusColor(props.row.status)"
                :label="props.row.status"
              />
            </q-td>
          </template>

          <template #body-cell-confirmations="props">
            <q-td :props="props">
              <div class="column q-gutter-xs">
                <q-badge
                  :color="props.row.parent_confirmed ? 'positive' : 'grey'"
                >
                  Parent: {{ props.row.parent_confirmed ? 'Confirmed' : 'Pending' }}
                </q-badge>

                <q-badge
                  :color="props.row.tutor_confirmed ? 'positive' : 'grey'"
                >
                  Tutor: {{ props.row.tutor_confirmed ? 'Confirmed' : 'Pending' }}
                </q-badge>
              </div>
            </q-td>
          </template>

          <template #body-cell-actions="props">
            <q-td :props="props">
              <q-btn
                flat
                round
                dense
                color="primary"
                icon="edit"
                @click="openEditDialog(props.row)"
              >
                <q-tooltip>Update demo</q-tooltip>
              </q-btn>

              <q-btn
                flat
                round
                dense
                color="grey-7"
                icon="visibility"
                @click="showDetails(props.row)"
              >
                <q-tooltip>View details</q-tooltip>
              </q-btn>
            </q-td>
          </template>
        </q-table>
      </div>

      <div v-else class="q-pa-xl text-center">
        <q-icon name="event_busy" size="55px" color="grey-5" />
        <div class="text-h6 q-mt-sm">No demos found</div>
        <div class="text-grey-7">
          Schedule your first demo to get started.
        </div>
      </div>
    </q-card>

    <!-- Create Demo Dialog -->
    <q-dialog v-model="createDialog" persistent>
      <q-card style="width: 600px; max-width: 95vw">
        <q-card-section class="row items-center">
          <div>
            <div class="text-h6 text-weight-bold">Schedule New Demo</div>
            <div class="text-caption text-grey-7">
              Select a lead, tutor and demo schedule.
            </div>
          </div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-form @submit.prevent="createDemo">
          <q-card-section>
            <div class="q-gutter-md">
              <q-select
                v-model="form.lead_id"
                :options="leadOptions"
                option-value="value"
                option-label="label"
                emit-value
                map-options
                outlined
                label="Select Parent Lead *"
                :rules="[val => !!val || 'Please select a lead']"
              />

              <q-select
                v-model="form.tutor_id"
                :options="tutorOptions"
                option-value="value"
                option-label="label"
                emit-value
                map-options
                clearable
                use-input
                input-debounce="0"
                outlined
                label="Assign Tutor"
              />

              <div class="row q-col-gutter-md">
                <div class="col-12 col-sm-6">
                  <q-input
                    v-model="form.demo_date"
                    outlined
                    type="date"
                    label="Demo Date *"
                    :rules="[val => !!val || 'Demo date is required']"
                  />
                </div>

                <div class="col-12 col-sm-6">
                  <q-input
                    v-model="form.demo_time"
                    outlined
                    type="time"
                    label="Demo Time"
                  />
                </div>
              </div>

              <q-input
                v-model="form.notes"
                outlined
                type="textarea"
                rows="3"
                label="Notes"
                placeholder="Demo instructions or additional information..."
              />
            </div>
          </q-card-section>

          <q-separator />

          <q-card-actions align="right" class="q-pa-md">
            <q-btn flat label="Cancel" color="grey-8" v-close-popup />
            <q-btn
              type="submit"
              color="primary"
              label="Schedule Demo"
              unelevated
              :loading="saving"
            />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>

    <!-- Update Demo Dialog -->
    <q-dialog v-model="editDialog" persistent>
      <q-card style="width: 600px; max-width: 95vw">
        <q-card-section class="row items-center">
          <div>
            <div class="text-h6 text-weight-bold">Update Demo</div>
            <div class="text-caption text-grey-7">
              Update tutor, status, confirmations and outcome.
            </div>
          </div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-form @submit.prevent="updateDemo">
          <q-card-section>
            <div class="q-gutter-md">
              <!-- Parent Name: Read Only -->
              <q-input
                :model-value="getLead(selectedDemo?.lead_id)?.parent_name || ''"
                outlined
                label="Parent Name"
                disable
              />

              <!-- Assigned Tutor -->
              <q-select
                v-model="editForm.tutor_id"
                :options="tutorOptions"
                option-value="value"
                option-label="label"
                emit-value
                map-options
                clearable
                use-input
                input-debounce="0"
                outlined
                label="Assigned Tutor"
              />

              <!-- Demo Status -->
              <q-select
                v-model="editForm.status"
                :options="demoStatusOptions"
                outlined
                label="Demo Status"
                emit-value
                map-options
              />

              <div class="text-subtitle2">Confirmation Status</div>

              <q-toggle
                v-model="editForm.parent_confirmed"
                label="Parent Confirmed"
                color="positive"
              />

              <q-toggle
                v-model="editForm.tutor_confirmed"
                label="Tutor Confirmed"
                color="positive"
              />

              <!-- <q-select
                v-model="editForm.result"
                :options="resultOptions"
                clearable
                outlined
                label="Demo Result"
              /> -->

              <q-input
                v-model="editForm.notes"
                outlined
                type="textarea"
                rows="3"
                label="Notes"
              />
            </div>
          </q-card-section>

          <q-separator />

          <q-card-actions align="right" class="q-pa-md">
            <q-btn flat label="Cancel" color="grey-8" v-close-popup />
            <q-btn
              type="submit"
              color="primary"
              label="Save Changes"
              unelevated
              :loading="saving"
            />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>

    <!-- Details Dialog -->
    <q-dialog v-model="detailsDialog">
      <q-card
        v-if="selectedDemo"
        style="width: 480px; max-width: 95vw"
      >
        <q-card-section>
          <div class="text-h6 text-weight-bold">Demo Details</div>
          <div class="text-caption text-grey-7">
            Demo #{{ selectedDemo.id }}
          </div>
        </q-card-section>

        <q-separator />

        <q-card-section class="q-gutter-md">
          <div>
            <strong>Parent:</strong>
            {{ getLead(selectedDemo.lead_id)?.parent_name || 'Unknown' }}
          </div>
          <div>
            <strong>Phone:</strong>
            {{ getLead(selectedDemo.lead_id)?.parent_phone || 'Not available' }}
          </div>
          <div>
            <strong>Student Class:</strong>
            {{ getLead(selectedDemo.lead_id)?.student_class || 'Not available' }}
          </div>
          <div>
            <strong>Tutor:</strong>
            {{ getTutor(selectedDemo.tutor_id)?.full_name || 'Not assigned' }}
          </div>
          <div><strong>Date:</strong> {{ formatDate(selectedDemo.demo_date) }}</div>
          <div><strong>Time:</strong> {{ formatTime(selectedDemo.demo_time) }}</div>
          <div><strong>Status:</strong> {{ selectedDemo.status }}</div>
          <div>
            <strong>Parent Confirmation:</strong>
            {{ selectedDemo.parent_confirmed ? 'Confirmed' : 'Pending' }}
          </div>
          <div>
            <strong>Tutor Confirmation:</strong>
            {{ selectedDemo.tutor_confirmed ? 'Confirmed' : 'Pending' }}
          </div>
          <div><strong>Result:</strong> {{ selectedDemo.result || 'Not recorded' }}</div>
          <div><strong>Notes:</strong> {{ selectedDemo.notes || 'No notes' }}</div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from './../boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// Data
const demos = ref([])
const leads = ref([])
const tutors = ref([])

// Loading states
const loading = ref(false)
const saving = ref(false)

// Filters
const search = ref('')
const statusFilter = ref('All')

// Dialogs
const createDialog = ref(false)
const editDialog = ref(false)
const detailsDialog = ref(false)

const selectedDemo = ref(null)

// Demo statuses
const statusOptions = [
  'All',
  'Scheduled',
  'Rescheduled',
  'Cancelled',
  'Demo Done'
]

const demoStatusOptions = [
  { label: 'Scheduled', value: 'Scheduled' },
  { label: 'Rescheduled', value: 'Rescheduled' },
  { label: 'Cancelled', value: 'Cancelled' },
  { label: 'Demo Done', value: 'Demo Done' }
]

// Demo results
// const resultOptions = [
//   'Interested',
//   'Not Interested',
//   'Follow-up Required',
//   'Tuition Closed',
//   'Pending'
// ]

// Table columns
const columns = [
  { name: 'id', label: 'Demo ID', field: 'id', align: 'left', sortable: true },
  { name: 'lead', label: 'Parent / Lead', field: 'lead_id', align: 'left' },
  { name: 'tutor', label: 'Tutor', field: 'tutor_id', align: 'left' },
  { name: 'date', label: 'Date & Time', field: 'demo_date', align: 'left', sortable: true },
  { name: 'status', label: 'Status', field: 'status', align: 'left' },
  // { name: 'result', label: 'Result', field: 'result', align: 'left' },
  { name: 'confirmations', label: 'Confirmations', field: 'parent_confirmed', align: 'left' },
  { name: 'notes', label: 'Notes', field: 'notes', align: 'left' },
  { name: 'actions', label: 'Actions', field: 'id', align: 'center' }
]

// Empty create form
const emptyCreateForm = () => ({
  lead_id: null,
  tutor_id: null,
  demo_date: '',
  demo_time: '',
  notes: ''
})

const form = ref(emptyCreateForm())

// Edit form
const editForm = ref({
  id: null,
  tutor_id: null,
  status: 'Scheduled',
  parent_confirmed: false,
  tutor_confirmed: false,
  result: null,
  notes: ''
})

// Only New Lead parents can be selected
const leadOptions = computed(() =>
  leads.value
    .filter(lead => lead.status === 'New Lead')
    .map(lead => ({
      value: lead.id,
      label: `${lead.parent_name} — ${lead.student_class || ''} — ${lead.parent_phone || ''}`
    }))
)

// Only active tutors
const tutorOptions = computed(() =>
  tutors.value
    .filter(tutor => tutor.is_active)
    .map(tutor => ({
      value: tutor.id,
      label: `${tutor.full_name} — ${tutor.phone || ''}`
    }))
)

// Filter demos
const filteredDemos = computed(() => {
  const query = search.value.toLowerCase().trim()

  return demos.value.filter(demo => {
    const lead = getLead(demo.lead_id)
    const tutor = getTutor(demo.tutor_id)

    const searchable = [
      demo.id,
      lead?.parent_name,
      lead?.parent_phone,
      lead?.student_class,
      lead?.location,
      tutor?.full_name,
      tutor?.phone,
      demo.status,
      demo.result,
      demo.notes
    ].join(' ').toLowerCase()

    const matchesSearch = searchable.includes(query)

    const matchesStatus =
      statusFilter.value === 'All' ||
      demo.status === statusFilter.value

    return matchesSearch && matchesStatus
  })
})

// Count demos by status
const countStatus = status =>
  demos.value.filter(demo => demo.status === status).length

// Find lead
const getLead = id =>
  leads.value.find(lead => lead.id === id)

// Find tutor
const getTutor = id =>
  tutors.value.find(tutor => tutor.id === id)

// Date formatting
const formatDate = value => {
  if (!value) return 'Not set'

  const date = new Date(`${value}T12:00:00`)

  return date.toLocaleDateString('en-PK', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

// Time formatting
const formatTime = value => {
  if (!value) return 'Time not set'

  const parts = value.split(':')
  const date = new Date()

  date.setHours(Number(parts[0]), Number(parts[1]), 0, 0)

  return date.toLocaleTimeString('en-PK', {
    hour: 'numeric',
    minute: '2-digit'
  })
}

// Status colors
const statusColor = status => {
  const colors = {
    Scheduled: 'primary',
    'Demo Done': 'positive',
    Rescheduled: 'warning',
    Cancelled: 'negative'
  }

  return colors[status] || 'grey'
}

// Load all required data
const fetchData = async () => {
  loading.value = true

  try {
    const [demoResponse, leadResponse, tutorResponse] = await Promise.all([
      api.get('/api/demos/'),
      api.get('/api/leads/'),
      api.get('/api/tutors/')
    ])

    demos.value = demoResponse.data
    leads.value = leadResponse.data
    tutors.value = tutorResponse.data
  } catch (error) {
    console.error('Error loading demo data:', error)

    $q.notify({
      type: 'negative',
      message: error.response?.data?.detail ||
        'Data load nahi ho saka. Backend aur API check karein.'
    })
  } finally {
    loading.value = false
  }
}

// Open Create Dialog
const openCreateDialog = () => {
  form.value = emptyCreateForm()
  createDialog.value = true
}

// Create Demo
const createDemo = async () => {
  saving.value = true

  try {
    const payload = {
      lead_id: form.value.lead_id,
      tutor_id: form.value.tutor_id || null,
      demo_date: form.value.demo_date,
      demo_time: form.value.demo_time || null,
      status: 'Scheduled',
      parent_confirmed: false,
      tutor_confirmed: false,
      result: null,
      notes: form.value.notes || null
    }

    await api.post('/api/demos/', payload)

    $q.notify({
      type: 'positive',
      message: 'Demo successfully scheduled!'
    })

    createDialog.value = false
    form.value = emptyCreateForm()

    await fetchData()
  } catch (error) {
    console.error('Error creating demo:', error)

    $q.notify({
      type: 'negative',
      message:
        error.response?.data?.detail ||
        'Demo save nahi ho saka. API check karein.'
    })
  } finally {
    saving.value = false
  }
}

// Open Edit Dialog
const openEditDialog = demo => {
  selectedDemo.value = demo

  editForm.value = {
    id: demo.id,
    tutor_id: demo.tutor_id,
    status: demo.status,
    parent_confirmed: demo.parent_confirmed,
    tutor_confirmed: demo.tutor_confirmed,
    result: demo.result,
    notes: demo.notes || ''
  }

  editDialog.value = true
}

// Update Demo
const updateDemo = async () => {
  saving.value = true

  try {
    const payload = {
      tutor_id: editForm.value.tutor_id || null,
      status: editForm.value.status,
      parent_confirmed: editForm.value.parent_confirmed,
      tutor_confirmed: editForm.value.tutor_confirmed,
      result: editForm.value.result || null,
      notes: editForm.value.notes || null
    }

    await api.patch(`/api/demos/${editForm.value.id}`, payload)

    $q.notify({
      type: 'positive',
      message: 'Demo successfully updated!'
    })

    editDialog.value = false

    await fetchData()
  } catch (error) {
    console.error('Error updating demo:', error)

    $q.notify({
      type: 'negative',
      message:
        error.response?.data?.detail ||
        'Demo update nahi ho saka.'
    })
  } finally {
    saving.value = false
  }
}

// Show Details
const showDetails = demo => {
  selectedDemo.value = demo
  detailsDialog.value = true
}

// Initial load
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.q-page {
  background: aliceblue;
}

.stat-card {
  border-radius: 12px;
}

:deep(.q-table th) {
  font-weight: 700;
  color: #64748b;
}

:deep(.q-table tbody td) {
  padding-top: 14px;
  padding-bottom: 14px;
}

@media (max-width: 600px) {
  .text-h4 {
    font-size: 25px;
  }
}
</style>
