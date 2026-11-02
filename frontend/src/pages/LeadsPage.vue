
<template>
    <q-page class="q-pa-md">
        <!-- Page Header -->
        <div class="row items-center justify-between q-mb-lg">
            <div>
                <div class="text-h5 text-weight-bold">All Leads</div>
                <div class="text-grey-7">
                    Manage parent inquiries and home tuition leads
                </div>
            </div>

            <q-btn
                color="primary"
                icon="add"
                label="Add New Lead"
                @click="openAddDialog"
            />
        </div>

        <!-- Statistics -->
        <div class="row q-col-gutter-md q-mb-lg">
            <div class="col-12 col-sm-4">
                <q-card flat bordered>
                    <q-card-section>
                        <div class="text-grey-7">Total Leads</div>
                        <div class="text-h4 text-weight-bold">
                            {{ leads.length }}
                        </div>
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
                    <q-input
                        v-model="search"
                        outlined
                        dense
                        clearable
                        placeholder="Search parent, phone, class or location..."
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
                        emit-value
                        map-options
                        label="Filter by status"
                    />
                </div>
            </q-card-section>

            <q-separator />

            <q-table
                :rows="filteredLeads"
                :columns="columns"
                row-key="id"
                :loading="loading"
                flat
                :pagination="{ rowsPerPage: 10 }"
                no-data-label="No leads found"
            >
                <!-- Lead ID -->
                <template #body-cell-lead_code="props">
                    <q-td :props="props">
                        <q-badge color="blue-1" text-color="primary">
                            {{ props.row.lead_code }}
                        </q-badge>
                    </q-td>
                </template>

                <!-- Parent Details -->
                <template #body-cell-parent_name="props">
                    <q-td :props="props">
                        <div class="text-weight-bold">
                            {{ props.row.parent_name || 'Not specified' }}
                        </div>
                        <div class="text-grey-7 text-caption">
                            {{ props.row.parent_phone }}
                        </div>
                    </q-td>
                </template>

                <!-- Class -->
                <template #body-cell-student_class="props">
                    <q-td :props="props">
                        {{ props.row.student_class || 'Not specified' }}
                    </q-td>
                </template>

                <!-- Location -->
                <template #body-cell-location="props">
                    <q-td :props="props">
                        {{ props.row.location || 'Not specified' }}
                    </q-td>
                </template>

                <!-- Subjects -->
                <template #body-cell-subjects="props">
                    <q-td :props="props">
                        {{ props.row.subjects || 'Not specified' }}
                    </q-td>
                </template>

                <!-- Budget -->
                <template #body-cell-monthly_budget="props">
                    <q-td :props="props">
                        {{
                            props.row.monthly_budget
                                ? 'Rs. ' + Number(props.row.monthly_budget).toLocaleString()
                                : 'Not specified'
                        }}
                    </q-td>
                </template>

                <!-- Status -->
                <template #body-cell-status="props">
                    <q-td :props="props">
                        <q-badge :color="statusColor(props.row.status)">
                            {{ props.row.status }}
                        </q-badge>
                    </q-td>
                </template>

                <!-- Created Date -->
                <template #body-cell-created_at="props">
                    <q-td :props="props">
                        {{ formatDate(props.row.created_at) }}
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
                            icon="edit"
                            @click="openEditDialog(props.row)"
                        >
                            <q-tooltip>Edit Lead</q-tooltip>
                        </q-btn>

                        <q-btn
                            flat
                            round
                            dense
                            color="negative"
                            icon="delete"
                            @click="deleteLead(props.row)"
                        >
                            <q-tooltip>Delete Lead</q-tooltip>
                        </q-btn>
                    </q-td>
                </template>
            </q-table>
        </q-card>

        <!-- Add / Edit Lead Dialog -->
        <q-dialog v-model="showDialog" persistent>
            <q-card style="width: 650px; max-width: 95vw">
                <q-card-section class="row items-center">
                    <div class="text-h6 text-weight-bold">
                        {{ isEditing ? 'Edit Lead' : 'Add New Lead' }}
                    </div>

                    <q-space />

                    <q-btn
                        icon="close"
                        flat
                        round
                        dense
                        :disable="saving"
                        @click="closeDialog"
                    />
                </q-card-section>

                <q-separator />

                <q-form @submit="saveLead">
                    <q-card-section>
                        <div class="row q-col-gutter-md">

                            <!-- Parent Name -->
                            <div class="col-12 col-md-6">
                                <q-input
                                    v-model="form.parent_name"
                                    label="Parent Name"
                                    outlined
                                    dense
                                    clearable
                                />
                            </div>

                            <!-- Parent Phone -->
                            <div class="col-12 col-md-6">
                                <q-input
                                    v-model="form.parent_phone"
                                    label="Parent Phone / WhatsApp *"
                                    outlined
                                    dense
                                    :rules="[
                                        val => !!String(val || '').trim() || 'Phone is required'
                                    ]"
                                />
                            </div>

                            <!-- Student Class -->
                            <div class="col-12 col-md-6">
                                <q-input
                                    v-model="form.student_class"
                                    label="Student Class"
                                    outlined
                                    dense
                                    clearable
                                />
                            </div>

                            <!-- Location -->
                            <div class="col-12 col-md-6">
                                <q-input
                                    v-model="form.location"
                                    label="Location / Area *"
                                    outlined
                                    dense
                                    placeholder="e.g. DHA Phase 6"
                                    :rules="[
                                        val => !!String(val || '').trim() || 'Location is required'
                                    ]"
                                />
                            </div>

                            <!-- Subjects -->
                            <div class="col-12 col-md-6">
                                <q-input
                                    v-model="form.subjects"
                                    label="Subjects"
                                    outlined
                                    dense
                                    placeholder="Maths, Physics, Chemistry"
                                />
                            </div>

                            <!-- Monthly Budget -->
                            <div class="col-12 col-md-6">
                                <q-input
                                    v-model.number="form.monthly_budget"
                                    label="Monthly Budget (PKR)"
                                    type="number"
                                    min="0"
                                    outlined
                                    dense
                                />
                            </div>

                            <!-- Status - Edit Only -->
                            <div
                                v-if="isEditing"
                                class="col-12"
                            >
                                <q-select
                                    v-model="form.status"
                                    :options="leadStatusOptions"
                                    label="Lead Status"
                                    outlined
                                    dense
                                    emit-value
                                    map-options
                                />
                            </div>

                            <!-- Notes -->
                            <div class="col-12">
                                <q-input
                                    v-model="form.notes"
                                    label="Notes"
                                    type="textarea"
                                    outlined
                                    rows="3"
                                />
                            </div>

                        </div>
                    </q-card-section>

                    <q-separator />

                    <q-card-actions align="right" class="q-pa-md">
                        <q-btn
                            label="Cancel"
                            flat
                            :disable="saving"
                            @click="closeDialog"
                        />

                        <q-btn
                            :label="isEditing ? 'Update Lead' : 'Save Lead'"
                            type="submit"
                            color="primary"
                            :loading="saving"
                        />
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

const $q = useQuasar()

// State
const leads = ref([])
const loading = ref(false)
const saving = ref(false)
const showDialog = ref(false)
const isEditing = ref(false)
const editingLeadId = ref(null)

const search = ref('')
const statusFilter = ref('All')

// Only these statuses can be manually selected for a Lead
const leadStatusOptions = [
    {
        label: 'New Lead',
        value: 'New Lead'
    },
    {
        label: 'Parent Not Responding',
        value: 'Parent Not Responding'
    },
    {
        label: 'Cancelled / Not Interested',
        value: 'Cancelled / Not Interested'
    }
]

// Filter options
const statusOptions = [
    {
        label: 'All Statuses',
        value: 'All'
    },
    ...leadStatusOptions
]

// Empty form
const emptyForm = () => ({
    parent_name: '',
    parent_phone: '',
    student_class: '',
    subjects: '',
    location: '',
    monthly_budget: null,
    notes: '',
    status: 'New Lead'
})

const form = ref(emptyForm())


// Search and status filtering
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
            lead.location,
            lead.notes
        ]
            .filter(Boolean)
            .join(' ')
            .toLowerCase()

        return matchesStatus && searchableText.includes(query)
    })
})

// Count status
function countStatus(status) {
    return leads.value.filter(lead => lead.status === status).length
}
// Status badge colors
function statusColor(status) {
    const colors = {
        'New Lead': 'blue',
        'Parent Not Responding': 'orange',
        'Cancelled / Not Interested': 'negative'
    }

    return colors[status] || 'grey'
}

// Date formatting
function formatDate(value) {
    if (!value) return '-'

    return new Date(value).toLocaleDateString('en-PK', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    })
}

// Fetch leads
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

// Open Add Dialog
function openAddDialog() {
    isEditing.value = false
    editingLeadId.value = null
    form.value = emptyForm()
    showDialog.value = true
}

// Open Edit Dialog
function openEditDialog(lead) {
    isEditing.value = true
    editingLeadId.value = lead.id

    form.value = {
        parent_name: lead.parent_name || '',
        parent_phone: lead.parent_phone || '',
        student_class: lead.student_class || '',
        subjects: lead.subjects || '',
        location: lead.location || '',
        monthly_budget: lead.monthly_budget ?? null,
        notes: lead.notes || '',
        status: lead.status || 'New Lead'
    }

    showDialog.value = true
}

// Close Dialog
function closeDialog() {
    if (saving.value) return

    showDialog.value = false
    form.value = emptyForm()
    isEditing.value = false
    editingLeadId.value = null
}

// Save Lead - Create or Update
async function saveLead() {
    saving.value = true

    try {
        const payload = {
            parent_name: form.value.parent_name.trim() || null,
            parent_phone: form.value.parent_phone.trim(),
            student_class: form.value.student_class.trim() || null,
            subjects: form.value.subjects.trim() || null,
            location: form.value.location.trim(),
            monthly_budget:
                form.value.monthly_budget === '' ||
                form.value.monthly_budget === null
                    ? null
                    : Number(form.value.monthly_budget),
            notes: form.value.notes.trim() || null
        }

        if (isEditing.value) {
            payload.status = form.value.status

            await api.put(
                `/api/leads/${editingLeadId.value}`,
                payload
            )

            $q.notify({
                type: 'positive',
                message: 'Lead successfully updated!'
            })
        } else {
            await api.post('/api/leads/', payload)

            $q.notify({
                type: 'positive',
                message: 'New lead successfully saved!'
            })
        }

        showDialog.value = false
        form.value = emptyForm()
        isEditing.value = false
        editingLeadId.value = null

        await fetchLeads()

    } catch (error) {
        console.error('Save lead error:', error)

        $q.notify({
            type: 'negative',
            message:
                error.response?.data?.detail ||
                'Lead save nahi ho saki.'
        })
    } finally {
        saving.value = false
    }
}

// Delete Lead
function deleteLead(lead) {
    $q.dialog({
        title: 'Delete Lead',
        message: `Are you sure you want to delete ${lead.lead_code}? This action cannot be undone.`,
        cancel: {
            label: 'Cancel',
            flat: true
        },
        ok: {
            label: 'Delete',
            color: 'negative'
        },
        persistent: true
    }).onOk(async () => {
        try {
            await api.delete(`/api/leads/${lead.id}`)

            $q.notify({
                type: 'positive',
                message: 'Lead successfully deleted!'
            })

            await fetchLeads()

        } catch (error) {
            console.error('Delete lead error:', error)

            $q.notify({
                type: 'negative',
                message:
                    error.response?.data?.detail ||
                    'Lead delete nahi ho saki.'
            })
        }
    })
}

// Load data on page mount
onMounted(() => {
    fetchLeads()
})

// Table columns
const columns = [
    // {name: 'lead_code',label: 'Lead ID',field: 'lead_code',align: 'left',sortable: true},
    {name: 'parent_name',label: 'Parent',field: 'parent_name',align: 'left',sortable: true},
    {
        name: 'student_class',
        label: 'Class',
        field: row => row.student_class || 'Not specified',
        align: 'left'
    },
    {
        name: 'location',
        label: 'Location',
        field: row => row.location || 'Not specified',
        align: 'left'
    },
    {
        name: 'subjects',
        label: 'Subjects',
        field: row => row.subjects || 'Not specified',
        align: 'left'
    },
    {
        name: 'monthly_budget',
        label: 'Budget',
        field: 'monthly_budget',
        align: 'left',
        sortable: true
    },
    {
        name: 'status',
        label: 'Status',
        field: 'status',
        align: 'left',
        sortable: true
    },
    {
        name: 'created_at',
        label: 'Created',
        field: 'created_at',
        align: 'left',
        sortable: true
    },
    {
        name: 'actions',
        label: 'Actions',
        field: 'actions',
        align: 'center'
    }
]
</script>

<style scoped>
.q-page {
    background: aliceblue;
}
</style>
