<template>
    <q-page class="q-pa-sm">
        <!-- Page Header -->
        <div class="row items-center justify-between q-mb-sm">
            <div>
                <div class="text-h5 text-weight-bold">All Leads</div>
                <div class="text-grey-7">
                    Manage parent inquiries and home tuition leads
                </div>
            </div>

            <q-btn color="primary" icon="add" label="Add New Lead" @click="openAddDialog" />
        </div>

        <!-- Statistics -->
        <div class="row q-col-gutter-md q-mb-sm">
            <div class="col-12 col-sm-4">
                <q-card flat bordered>
                    <q-card-section>
                        <div class="text-grey-7">Total Leads</div>
                        <div class="text-h4 text-weight-bold">{{ leads.length }}</div>
                    </q-card-section>
                </q-card>
            </div>

            <div class="col-12 col-sm-4">
                <q-card flat bordered>
                    <q-card-section>
                        <div class="text-grey-7">New Leads</div>
                        <div class="text-h4 text-weight-bold text-primary">
                            {{ countStatus('New Lead') }}
                        </div>
                    </q-card-section>
                </q-card>
            </div>

            <div class="col-12 col-sm-4">
                <q-card flat bordered>
                    <q-card-section>
                        <div class="text-grey-7">Tuition Closed</div>
                        <div class="text-h4 text-weight-bold text-positive">
                            {{ countStatus('Tuition Closed') }}
                        </div>
                    </q-card-section>
                </q-card>
            </div>
        </div>

        <!-- Leads Table -->
        <q-card flat bordered>
            <q-card-section class="row items-center q-col-gutter-md">
                <div class="col-12 col-md-7">
                    <q-input v-model="search" outlined dense clearable
                        placeholder="Search parent, phone, class or location...">
                        <template #prepend>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </div>

                <div class="col-12 col-md-5">
                    <q-select v-model="statusFilter" :options="statusOptions" outlined dense emit-value map-options
                        label="Filter by status" />
                </div>
            </q-card-section>

            <q-separator />

            <q-table :rows="filteredLeads" :columns="columns" row-key="id" :loading="loading" flat
                :pagination="{ rowsPerPage: 10 }" no-data-label="No leads found">
                <template #body-cell-parent_name="props">
                    <q-td :props="props">
                        <div class="text-weight-bold">{{ props.row.parent_name }}</div>
                        <div class="text-grey-7 text-caption">
                            {{ props.row.parent_phone }}
                        </div>
                    </q-td>
                </template>

                <template #body-cell-lead_code="props">
                    <q-td :props="props">
                        <q-badge color="blue-1" text-color="primary">
                            {{ props.row.lead_code }}
                        </q-badge>
                    </q-td>
                </template>

                <template #body-cell-status="props">
                    <q-td :props="props">
                        <q-badge :color="statusColor(props.row.status)">
                            {{ props.row.status }}
                        </q-badge>
                    </q-td>
                </template>

                <template #body-cell-monthly_budget="props">
                    <q-td :props="props">
                        {{ props.row.monthly_budget
                            ? 'Rs. ' + props.row.monthly_budget.toLocaleString()
                            : 'Not specified' }}
                    </q-td>
                </template>

                <template #body-cell-created_at="props">
                    <q-td :props="props">
                        {{ formatDate(props.row.created_at) }}
                    </q-td>
                </template>
            </q-table>
        </q-card>

        <!-- Add Lead Dialog -->
        <q-dialog v-model="showDialog" persistent>
            <q-card style="width: 650px; max-width: 95vw">
                <q-card-section class="row items-center">
                    <div class="text-h6 text-weight-bold">Add New Lead</div>
                    <q-space />
                    <q-btn icon="close" flat round dense v-close-popup />
                </q-card-section>

                <q-separator />

                <q-form @submit="createLead">
                    <q-card-section>
                        <div class="row q-col-gutter-md">

                            <div class="col-12 col-md-6">
                                <q-input v-model="form.parent_name" label="Parent Name *" outlined dense
                                    :rules="[val => !!val || 'Parent name is required']" />
                            </div>

                            <div class="col-12 col-md-6">
                                <q-input v-model="form.parent_phone" label="Parent Phone / WhatsApp *" outlined dense
                                    :rules="[val => !!val || 'Phone is required']" />
                            </div>

                            <div class="col-12 col-md-6">
                                <q-input v-model="form.student_class" label="Student Class *" outlined dense
                                    :rules="[val => !!val || 'Class is required']" />
                            </div>

                            <div class="col-12 col-md-6">
                                <q-input v-model="form.location" label="Location / Area" outlined dense
                                    placeholder="e.g. DHA Phase 6" />
                            </div>

                            <div class="col-12 col-md-6">
                                <q-input v-model="form.subjects" label="Subjects" outlined dense
                                    placeholder="Maths, Physics, Chemistry" />
                            </div>

                            <div class="col-12 col-md-6">
                                <q-input v-model.number="form.monthly_budget" label="Monthly Budget (PKR)" type="number"
                                    min="0" outlined dense />
                            </div>

                            <div class="col-12">
                                <q-input v-model="form.notes" label="Notes" type="textarea" outlined rows="3" />
                            </div>

                        </div>
                    </q-card-section>

                    <q-separator />

                    <q-card-actions align="right" class="q-pa-md">
                        <q-btn label="Cancel" flat v-close-popup />
                        <q-btn label="Save Lead" type="submit" color="primary" :loading="saving" />
                    </q-card-actions>
                </q-form>
            </q-card>
        </q-dialog>

    </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { api } from './../boot/axios'
import { Notify } from 'quasar'

const $q = useQuasar()

const leads = ref([])
const loading = ref(false)
const saving = ref(false)
const showDialog = ref(false)
const search = ref('')
const statusFilter = ref('All')

const statusOptions = [
    { label: 'All Statuses', value: 'All' },
    { label: 'New Lead', value: 'New Lead' },
    { label: 'Tutor Assigned', value: 'Tutor Assigned' },
    { label: 'Demo Scheduled', value: 'Demo Scheduled' },
    { label: 'Demo Completed', value: 'Demo Completed' },
    { label: 'Follow-up', value: 'Follow-up' },
    { label: 'Tuition Closed', value: 'Tuition Closed' },
    { label: 'Lost', value: 'Lost' }
]

const emptyForm = () => ({
    parent_name: '',
    parent_phone: '',
    student_class: '',
    subjects: '',
    location: '',
    monthly_budget: null,
    notes: ''
})

const form = ref(emptyForm())

const filteredLeads = computed(() => {
    const query = search.value.toLowerCase().trim()

    return leads.value.filter(lead => {
        const matchesStatus =
            statusFilter.value === 'All' ||
            lead.status === statusFilter.value

        const searchableText = [
            lead.lead_code,
            lead.parent_name,
            lead.parent_phone,
            lead.student_class,
            lead.subjects,
            lead.location
        ].join(' ').toLowerCase()

        return matchesStatus && searchableText.includes(query)
    })
})

function countStatus(status) {
    return leads.value.filter(lead => lead.status === status).length
}

function statusColor(status) {
    const colors = {
        'New Lead': 'blue',
        'Tutor Assigned': 'purple',
        'Demo Scheduled': 'orange',
        'Demo Completed': 'teal',
        'Follow-up': 'deep-orange',
        'Tuition Closed': 'positive',
        'Lost': 'negative'
    }

    return colors[status] || 'grey'
}

function formatDate(value) {
    if (!value) return '-'

    return new Date(value).toLocaleDateString('en-PK', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    })
}

async function fetchLeads() {
    loading.value = true

    try {
        const response = await api.get('/api/leads/')
        leads.value = response.data
    } catch (error) {
        console.error('Fetch leads error:', error)

        $q.notify({
            type: 'negative',
            message: 'Leads load nahi ho sake. Backend check karein.'
        })
    } finally {
        loading.value = false
    }
}

function openAddDialog() {
    form.value = emptyForm()
    showDialog.value = true
}

async function createLead() {
    saving.value = true
    try {
        const payload = {
            parent_name: form.value.parent_name.trim(),
            parent_phone: form.value.parent_phone.trim(),
            student_class: form.value.student_class.trim(),
            subjects: form.value.subjects || null,
            location: form.value.location || null,
            monthly_budget: form.value.monthly_budget || null,
            notes: form.value.notes || null
        }

        await api.post('/api/leads/', payload)

        showDialog.value = false

        $q.notify({
            type: 'positive',
            message: 'New lead successfully saved!'
        })

        await fetchLeads()

    } catch (error) {
        console.error('Create lead error:', error)

        $q.notify({
            type: 'negative',
            message: error.response?.data?.detail || 'Lead save nahi ho saki.'
        })
    } finally {
        saving.value = false
    }
}

onMounted(() => {
    fetchLeads()
})

const columns = [
    {name: 'lead_code',label: 'Lead ID',field: 'lead_code',align: 'left',sortable: true},
    {name: 'parent_name',label: 'Parent',field: 'parent_name',align: 'left',sortable: true},
    {name: 'student_class',label: 'Class',field: 'student_class',align: 'left',sortable: true},
    {name: 'location',label: 'Location',field: row => row.location || 'Not specified',align: 'left'},
    {name: 'subjects',label: 'Subjects',field: row => row.subjects || 'Not specified',align: 'left'},
    {name: 'monthly_budget',label: 'Budget',field: 'monthly_budget',align: 'left',sortable: true},
    {name: 'status',label: 'Status',field: 'status',align: 'left',sortable: true},
    {name: 'created_at',label: 'Created',field: 'created_at',align: 'left',sortable: true},
    {name: 'notes',label: 'Notes',field: 'notes',align: 'left',sortable: true}
]
</script>

<style scoped>
.q-page {
    background: aliceblue;
}
</style>
