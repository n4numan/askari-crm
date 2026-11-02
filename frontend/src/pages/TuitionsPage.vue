
<template>
  <q-page class="q-pa-md">
    <!-- Header -->
    <div class="row items-center justify-between q-mb-lg">
      <div>
        <div class="text-overline text-grey-7">ACADEMY MANAGEMENT</div>
        <div class="text-h4 text-weight-bold">Tuitions</div>
        <div class="text-grey-7 q-mt-xs">
          Manage confirmed tuition records and monthly fees.
        </div>
      </div>

      <q-btn
        color="primary"
        icon="add"
        label="Add Tuition"
        unelevated
        @click="openCreateDialog"
      />
    </div>

    <!-- Statistics -->
    <div class="row q-col-gutter-md q-mb-lg">
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-grey-7">Total Tuitions</div>
            <div class="text-h4 text-weight-bold q-mt-sm">
              {{ tuitions.length }}
            </div>
            <q-icon name="school" color="primary" size="28px" />
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-grey-7">Active</div>
            <div class="text-h4 text-weight-bold text-positive q-mt-sm">
              {{ countByStatus('Active') }}
            </div>
            <q-icon name="check_circle" color="positive" size="28px" />
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-grey-7">Completed</div>
            <div class="text-h4 text-weight-bold text-blue q-mt-sm">
              {{ countByStatus('Completed') }}
            </div>
            <q-icon name="task_alt" color="blue" size="28px" />
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-grey-7">Monthly Fee Total</div>
            <div class="text-h4 text-weight-bold q-mt-sm">
              {{ formatCurrency(totalMonthlyFee) }}
            </div>
            <div class="text-caption text-grey-7">
              Active tuition records
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Filters and Table -->
    <q-card flat bordered>
      <q-card-section>
        <div class="row q-col-gutter-md items-center">
          <div class="col-12 col-md-6">
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

          <div class="col-12 col-md-3">
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

      <q-table
        :rows="filteredTuitions"
        :columns="columns"
        row-key="id"
        :loading="loading"
        flat
        :pagination="{ rowsPerPage: 10 }"
        no-data-label="No tuition records found"
      >
        <!-- Lead -->
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

        <!-- Tutor -->
        <template #body-cell-tutor="props">
          <q-td :props="props">
            {{ getTutorName(props.row.tutor_id) }}
          </q-td>
        </template>

        <!-- Monthly fee -->
        <template #body-cell-monthly_fee="props">
          <q-td :props="props">
            <div class="text-weight-bold">
              {{ formatCurrency(props.row.monthly_fee) }}
            </div>
          </q-td>
        </template>

        <!-- Commission -->
        <template #body-cell-academy_commission="props">
          <q-td :props="props">
            {{ formatCurrency(props.row.academy_commission) }}
          </q-td>
        </template>

        <!-- Status -->
        <template #body-cell-status="props">
          <q-td :props="props">
            <q-badge
              :color="statusColor(props.row.status)"
              :label="props.row.status"
              class="q-pa-sm"
            />
          </q-td>
        </template>

        <!-- Closing date -->
        <template #body-cell-closing_date="props">
          <q-td :props="props">
            {{ formatDate(props.row.closing_date) }}
          </q-td>
        </template>

        <!-- Actions -->
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

    <!-- Create Tuition Dialog -->
    <q-dialog v-model="createDialog" persistent>
      <q-card style="width: 700px; max-width: 95vw">
        <q-card-section class="row items-center">
          <div class="text-h6 text-weight-bold">Add New Tuition</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section>
          <q-form @submit.prevent="createTuition">
            <div class="row q-col-gutter-md">

              <!-- Lead -->
              <div class="col-12">
                <q-select
                  v-model="form.lead_id"
                  :options="availableLeadOptions"
                  emit-value
                  map-options
                  outlined
                  label="Select Closed Lead *"
                  :rules="[val => !!val || 'Please select a lead']"
                />
                <div class="text-caption text-grey-7 q-mt-xs">
                  Leads that already have a tuition record are excluded.
                </div>
              </div>

              <!-- Tutor -->
              <div class="col-12">
                <q-select
                  v-model="form.tutor_id"
                  :options="tutorOptions"
                  emit-value
                  map-options
                  outlined
                  clearable
                  label="Assigned Tutor (Optional)"
                />
              </div>

              <!-- Fee -->
              <div class="col-12 col-sm-6">
                <q-input
                  v-model.number="form.monthly_fee"
                  type="number"
                  min="1"
                  outlined
                  label="Monthly Fee (PKR) *"
                  prefix="Rs."
                  :rules="[
                    val => val !== null && val > 0 || 'Enter monthly fee'
                  ]"
                />
              </div>

              <!-- Commission -->
              <div class="col-12 col-sm-6">
                <q-input
                  v-model.number="form.academy_commission"
                  type="number"
                  min="0"
                  outlined
                  label="Academy Commission (PKR)"
                  prefix="Rs."
                />
              </div>

              <!-- Dates -->
              <div class="col-12 col-sm-6">
                <q-input
                  v-model="form.closing_date"
                  type="date"
                  outlined
                  label="Closing Date"
                />
              </div>

              <div class="col-12 col-sm-6">
                <q-input
                  v-model="form.start_date"
                  type="date"
                  outlined
                  label="Tuition Start Date"
                />
              </div>

              <div class="col-12 col-sm-6">
                <q-input
                  v-model="form.end_date"
                  type="date"
                  outlined
                  label="Tuition End Date"
                />
              </div>

              <!-- Status -->
              <div class="col-12 col-sm-6">
                <q-select
                  v-model="form.status"
                  :options="['Active', 'Completed', 'Cancelled', 'On Hold']"
                  outlined
                  label="Tuition Status"
                />
              </div>

              <!-- Notes -->
              <div class="col-12">
                <q-input
                  v-model="form.notes"
                  type="textarea"
                  outlined
                  rows="3"
                  label="Notes"
                  placeholder="Additional tuition details..."
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
                label="Save Tuition"
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
      <q-card style="width: 600px; max-width: 95vw">
        <q-card-section class="row items-center">
          <div class="text-h6 text-weight-bold">Tuition Details</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section v-if="selectedTuition">
          <div class="row q-col-gutter-md">
            <div class="col-12">
              <div class="text-caption text-grey-7">Lead / Parent</div>
              <div class="text-subtitle1 text-weight-bold">
                {{ getLeadName(selectedTuition.lead_id) }}
              </div>
              <div class="text-caption text-grey-7">
                {{ getLeadCode(selectedTuition.lead_id) }}
              </div>
            </div>

            <div class="col-12">
              <q-separator />
            </div>

            <div class="col-6">
              <div class="text-caption text-grey-7">Assigned Tutor</div>
              <div class="text-weight-medium">
                {{ getTutorName(selectedTuition.tutor_id) }}
              </div>
            </div>

            <div class="col-6">
              <div class="text-caption text-grey-7">Status</div>
              <q-badge
                :color="statusColor(selectedTuition.status)"
                :label="selectedTuition.status"
                class="q-pa-sm"
              />
            </div>

            <div class="col-6">
              <div class="text-caption text-grey-7">Monthly Fee</div>
              <div class="text-weight-bold">
                {{ formatCurrency(selectedTuition.monthly_fee) }}
              </div>
            </div>

            <div class="col-6">
              <div class="text-caption text-grey-7">Academy Commission</div>
              <div class="text-weight-bold">
                {{ formatCurrency(selectedTuition.academy_commission) }}
              </div>
            </div>

            <div class="col-6">
              <div class="text-caption text-grey-7">Closing Date</div>
              <div>{{ formatDate(selectedTuition.closing_date) }}</div>
            </div>

            <div class="col-6">
              <div class="text-caption text-grey-7">Start Date</div>
              <div>{{ formatDate(selectedTuition.start_date) }}</div>
            </div>

            <div class="col-6">
              <div class="text-caption text-grey-7">End Date</div>
              <div>{{ formatDate(selectedTuition.end_date) }}</div>
            </div>

            <div class="col-12">
              <div class="text-caption text-grey-7">Notes</div>
              <div>{{ selectedTuition.notes || 'No notes added' }}</div>
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


const tuitions = ref([])
const leads = ref([])
const tutors = ref([])

const loading = ref(false)
const saving = ref(false)

const search = ref('')
const statusFilter = ref('All')

const createDialog = ref(false)
const detailsDialog = ref(false)
const selectedTuition = ref(null)

const statusOptions = [
  { label: 'All statuses', value: 'All' },
  { label: 'Active', value: 'Active' },
  { label: 'Completed', value: 'Completed' },
  { label: 'Cancelled', value: 'Cancelled' },
  { label: 'On Hold', value: 'On Hold' }
]

const columns = [
  { name: 'lead', label: 'Lead / Parent', field: 'lead_id', align: 'left' },
  { name: 'tutor', label: 'Tutor', field: 'tutor_id', align: 'left' },
  { name: 'monthly_fee', label: 'Monthly Fee', field: 'monthly_fee', align: 'left', sortable: true },
  { name: 'academy_commission', label: 'Commission', field: 'academy_commission', align: 'left' },
  // { name: 'closing_date', label: 'Closing Date', field: 'closing_date', align: 'left', sortable: true },
  { name: 'start_date', label: 'Start Date', field: 'start_date', align: 'left', sortable: true },
  { name: 'end_date', label: 'End Date', field: 'end_date', align: 'left', sortable: true },
  { name: 'status', label: 'Status', field: 'status', align: 'left' },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const emptyForm = () => ({
  lead_id: null,
  tutor_id: null,
  monthly_fee: null,
  academy_commission: null,
  closing_date: '',
  start_date: '',
  end_date: '',
  status: 'Active',
  notes: ''
})

const form = ref(emptyForm())

// Exclude leads that already have a tuition record.
const availableLeadOptions = computed(() => {
  const existingLeadIds = new Set(
    tuitions.value.map(item => item.lead_id)
  )

  return leads.value
    .filter(lead => !existingLeadIds.has(lead.id))
    .map(lead => ({
      label: `${lead.lead_code} - ${lead.parent_name} (${lead.student_class})`,
      value: lead.id
    }))
})

const tutorOptions = computed(() =>
  tutors.value
    .filter(tutor => tutor.is_active)
    .map(tutor => ({
      label: `${tutor.full_name} - ${tutor.phone}`,
      value: tutor.id
    }))
)

const filteredTuitions = computed(() => {
  const query = search.value.toLowerCase().trim()

  return tuitions.value.filter(item => {
    const lead = leads.value.find(l => l.id === item.lead_id)
    const tutor = tutors.value.find(t => t.id === item.tutor_id)

    const searchText = [
      lead?.lead_code,
      lead?.parent_name,
      lead?.parent_phone,
      lead?.student_class,
      lead?.location,
      tutor?.full_name,
      item.notes
    ].join(' ').toLowerCase()

    const matchesSearch = !query || searchText.includes(query)

    const matchesStatus =
      statusFilter.value === 'All' ||
      item.status === statusFilter.value

    return matchesSearch && matchesStatus
  })
})

const totalMonthlyFee = computed(() =>
  tuitions.value
    .filter(item => item.status === 'Active')
    .reduce((total, item) => total + Number(item.monthly_fee || 0), 0)
)

function countByStatus(status) {
  return tuitions.value.filter(item => item.status === status).length
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

function formatCurrency(value) {
  if (value === null || value === undefined || value === '') {
    return '—'
  }

  return 'Rs. ' + Number(value).toLocaleString('en-PK')
}

function formatDate(value) {
  if (!value) return '—'

  const date = new Date(`${value}T12:00:00`)

  return date.toLocaleDateString('en-PK', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

function statusColor(status) {
  const colors = {
    Active: 'positive',
    Completed: 'blue',
    Cancelled: 'negative',
    'On Hold': 'orange'
  }

  return colors[status] || 'grey'
}

async function loadData() {
  loading.value = true

  try {
    const [tuitionRes, leadRes, tutorRes] = await Promise.all([
      api.get('/api/tuitions/'),
      api.get('/api/leads/'),
      api.get('/api/tutors/')
    ])

    tuitions.value = tuitionRes.data
    leads.value = leadRes.data
    tutors.value = tutorRes.data
  } catch (error) {
    console.error('Tuitions loading error:', error)

    window.alert(
      error.response?.data?.detail ||
      'Tuition records load nahi ho sake. Backend check karein.'
    )
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  form.value = emptyForm()
  createDialog.value = true
}

async function createTuition() {
  if (!form.value.lead_id || !form.value.monthly_fee) return

  saving.value = true

  try {
    const payload = {
      lead_id: form.value.lead_id,
      tutor_id: form.value.tutor_id || null,
      monthly_fee: Number(form.value.monthly_fee),
      academy_commission:
        form.value.academy_commission === null ||
        form.value.academy_commission === ''
          ? null
          : Number(form.value.academy_commission),
      closing_date: form.value.closing_date || null,
      start_date: form.value.start_date || null,
      end_date: form.value.end_date || null,
      status: form.value.status,
      notes: form.value.notes || null
    }

    await api.post('/api/tuitions/', payload)

    createDialog.value = false
    await loadData()

    window.alert('Tuition successfully created.')
  } catch (error) {
    console.error('Tuition creation error:', error)

    window.alert(
      error.response?.data?.detail ||
      'Tuition create nahi ho saki.'
    )
  } finally {
    saving.value = false
  }
}

function openDetails(item) {
  selectedTuition.value = item
  detailsDialog.value = true
}

onMounted(loadData)
</script>

<style scoped>
.q-page {
    background: aliceblue;
}
</style>
