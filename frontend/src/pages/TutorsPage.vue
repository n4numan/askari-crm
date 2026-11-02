<template>
    <q-page class="q-pa-sm">
        <!-- Page Header -->
        <div class="row items-center justify-between q-mb-md">
            <div>
                <div class="text-caption text-grey-7">TUTOR MANAGEMENT</div>
                <div class="text-h4 text-weight-bold">Tutors</div>
                <!-- <div class="text-grey-7 q-mt-xs">
                    Manage your registered home tutors.
                </div> -->
            </div>

            <q-btn color="primary" icon="person_add" label="Add Tutor" unelevated @click="openDialog" />
        </div>

        <!-- Statistics -->
        <div class="row q-col-gutter-md q-mb-md">
            <div class="col-12 col-sm-4">
                <q-card flat bordered class="stat-card">
                    <q-card-section>
                        <div class="text-grey-7">Total Tutors</div>
                        <div class="text-h4 text-weight-bold">{{ tutors.length }}</div>
                    </q-card-section>
                </q-card>
            </div>

            <div class="col-12 col-sm-4">
                <q-card flat bordered class="stat-card">
                    <q-card-section>
                        <div class="text-grey-7">Active Tutors</div>
                        <div class="text-h4 text-weight-bold text-positive">
                            {{ activeTutors }}
                        </div>
                    </q-card-section>
                </q-card>
            </div>

            <div class="col-12 col-sm-4">
                <q-card flat bordered class="stat-card">
                    <q-card-section>
                        <div class="text-grey-7">Inactive Tutors</div>
                        <div class="text-h4 text-weight-bold text-negative">
                            {{ tutors.length - activeTutors }}
                        </div>
                    </q-card-section>
                </q-card>
            </div>
        </div>

        <!-- Search and Filters -->
        <q-card flat bordered>
            <q-card-section>
                <div class="row q-col-gutter-md">
                    <div class="col-12 col-md-8">
                        <q-input v-model="search" outlined dense clearable
                            placeholder="Search tutor name, phone, subjects or area...">
                            <template #prepend>
                                <q-icon name="search" />
                            </template>
                        </q-input>
                    </div>

                    <div class="col-12 col-md-4">
                        <q-select v-model="statusFilter" :options="['All', 'Active', 'Inactive']" outlined dense
                            label="Tutor Status" />
                    </div>
                </div>
            </q-card-section>

            <q-separator />

            <!-- Loading -->
            <div v-if="loading" class="q-pa-xl text-center">
                <q-spinner-dots color="primary" size="40px" />
                <div class="text-grey-7 q-mt-sm">Loading tutors...</div>
            </div>

            <!-- Tutor Cards -->
            <div v-else-if="filteredTutors.length" class="row q-col-gutter-md q-pa-md">
                <div v-for="tutor in filteredTutors" :key="tutor.id" class="col-12 col-sm-6 col-lg-4">
                    <q-card flat bordered class="tutor-card full-height">
                        <q-card-section>
                            <div class="row items-center no-wrap">
                                <q-avatar color="primary" text-color="white" size="48px">
                                    {{ getInitials(tutor.full_name) }}
                                </q-avatar>

                                <div class="q-ml-md col">
                                    <div class="text-subtitle1 text-weight-bold">
                                        {{ tutor.full_name }}
                                    </div>
                                    <div class="text-caption text-grey-7">
                                        Tutor ID: #{{ tutor.id }}
                                    </div>
                                </div>

                                <q-badge :color="tutor.is_active ? 'positive' : 'negative'"
                                    :label="tutor.is_active ? 'Active' : 'Inactive'" />
                            </div>
                        </q-card-section>

                        <q-separator />

                        <q-card-section class="q-gutter-sm">
                            <div class="row items-center">
                                <q-icon name="phone" color="grey-7" class="q-mr-sm" />
                                <span>{{ tutor.phone }}</span>
                            </div>

                            <div class="row items-center" v-if="tutor.email">
                                <q-icon name="email" color="grey-7" class="q-mr-sm" />
                                <span>{{ tutor.email }}</span>
                            </div>

                            <div class="row items-start">
                                <q-icon name="menu_book" color="grey-7" class="q-mr-sm q-mt-xs" />
                                <div>
                                    <div class="text-caption text-grey-7">Subjects</div>
                                    {{ tutor.subjects || 'Not added' }}
                                </div>
                            </div>

                            <div class="row items-start">
                                <q-icon name="location_on" color="grey-7" class="q-mr-sm q-mt-xs" />
                                <div>
                                    <div class="text-caption text-grey-7">Teaching Areas</div>
                                    {{ tutor.areas || 'Not added' }}
                                </div>
                            </div>

                            <div class="row items-center">
                                <q-icon name="payments" color="grey-7" class="q-mr-sm" />
                                <span>
                                    Monthly Fee:
                                    <strong>
                                        {{ formatFee(tutor.monthly_fee) }}
                                    </strong>
                                </span>
                            </div>
                        </q-card-section>

                        <q-separator />

                        <q-card-actions align="right">
                            <q-btn flat dense color="primary" icon="visibility" label="Details"
                                @click="showDetails(tutor)" />
                        </q-card-actions>
                    </q-card>
                </div>
            </div>

            <!-- Empty State -->
            <div v-else class="q-pa-xl text-center">
                <q-icon name="person_search" size="55px" color="grey-5" />
                <div class="text-h6 q-mt-sm">No tutors found</div>
                <div class="text-grey-7">
                    Add a new tutor or change your search.
                </div>
            </div>
        </q-card>

        <!-- Add Tutor Dialog -->
        <q-dialog v-model="dialog" persistent>
            <q-card style="width: 600px; max-width: 95vw">
                <q-card-section class="row items-center">
                    <div>
                        <div class="text-h6 text-weight-bold">Add New Tutor</div>
                        <div class="text-caption text-grey-7">
                            Enter tutor information below.
                        </div>
                    </div>
                    <q-space />
                    <q-btn icon="close" flat round dense v-close-popup />
                </q-card-section>

                <q-separator />

                <q-form @submit.prevent="createTutor">
                    <q-card-section>
                        <div class="row q-col-gutter-md">
                            <div class="col-12">
                                <q-input v-model="form.full_name" outlined label="Full Name *"
                                    :rules="[val => !!val || 'Name is required']" />
                            </div>

                            <div class="col-12 col-sm-6">
                                <q-input v-model="form.phone" outlined label="Phone Number *" placeholder="03XX-XXXXXXX"
                                    :rules="[val => !!val || 'Phone is required']" />
                            </div>

                            <div class="col-12 col-sm-6">
                                <q-input v-model="form.email" outlined label="Email Address" type="email" />
                            </div>

                            <div class="col-12">
                                <q-input v-model="form.subjects" outlined label="Subjects"
                                    placeholder="Mathematics, Physics, Chemistry" />
                            </div>

                            <div class="col-12">
                                <q-input v-model="form.areas" outlined label="Teaching Areas"
                                    placeholder="DHA, Askari 10, Cantt" />
                            </div>

                            <div class="col-12">
                                <q-input v-model.number="form.monthly_fee" outlined type="number" min="0"
                                    label="Monthly Fee (PKR)" />
                            </div>

                            <div class="col-12">
                                <q-banner class="bg-grey-2 text-grey-8 rounded-borders">
                                    CNIC and CV file upload will be added in a later step.
                                </q-banner>
                            </div>
                        </div>
                    </q-card-section>

                    <q-separator />

                    <q-card-actions align="right" class="q-pa-md">
                        <q-btn flat label="Cancel" color="grey-8" v-close-popup />

                        <q-btn type="submit" color="primary" label="Save Tutor" unelevated :loading="saving" />
                    </q-card-actions>
                </q-form>
            </q-card>
        </q-dialog>

        <!-- Tutor Details Dialog -->
        <q-dialog v-model="detailsDialog">
            <q-card style="width: 450px; max-width: 95vw" v-if="selectedTutor">
                <q-card-section>
                    <div class="text-h6 text-weight-bold">
                        {{ selectedTutor.full_name }}
                    </div>
                    <div class="text-caption text-grey-7">
                        Tutor ID: #{{ selectedTutor.id }}
                    </div>
                </q-card-section>

                <q-separator />

                <q-card-section class="q-gutter-md">
                    <div><strong>Phone:</strong> {{ selectedTutor.phone }}</div>
                    <div><strong>Email:</strong> {{ selectedTutor.email || 'Not added' }}</div>
                    <div><strong>Subjects:</strong> {{ selectedTutor.subjects || 'Not added' }}</div>
                    <div><strong>Areas:</strong> {{ selectedTutor.areas || 'Not added' }}</div>
                    <div><strong>Monthly Fee:</strong> {{ formatFee(selectedTutor.monthly_fee) }}</div>
                    <div>
                        <strong>Status:</strong>
                        {{ selectedTutor.is_active ? 'Active' : 'Inactive' }}
                    </div>
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

// Page state
const tutors = ref([])
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const statusFilter = ref('All')

// Dialog state
const dialog = ref(false)
const detailsDialog = ref(false)
const selectedTutor = ref(null)

// Tutor form
const emptyForm = () => ({
    full_name: '',
    phone: '',
    email: '',
    subjects: '',
    areas: '',
    monthly_fee: null
})

const form = ref(emptyForm())

// Statistics
const activeTutors = computed(() =>
    tutors.value.filter(tutor => tutor.is_active).length
)

// Search and status filtering
const filteredTutors = computed(() => {
    const query = search.value.toLowerCase().trim()

    return tutors.value.filter(tutor => {
        const matchesSearch = [
            tutor.full_name,
            tutor.phone,
            tutor.email,
            tutor.subjects,
            tutor.areas
        ]
            .join(' ')
            .toLowerCase()
            .includes(query)

        const matchesStatus =
            statusFilter.value === 'All' ||
            (statusFilter.value === 'Active' && tutor.is_active) ||
            (statusFilter.value === 'Inactive' && !tutor.is_active)

        return matchesSearch && matchesStatus
    })
})

// Load tutors from backend
const fetchTutors = async () => {
    loading.value = true

    try {
        const response = await api.get('/api/tutors/')
        tutors.value = response.data
    } catch (error) {
        console.error('Error loading tutors:', error)

        $q.notify({
            type: 'negative',
            message: 'Tutors load nahi ho sake. Backend check karein.'
        })
    } finally {
        loading.value = false
    }
}

// Open add tutor dialog
const openDialog = () => {
    form.value = emptyForm()
    dialog.value = true
}

// Save tutor to database
const createTutor = async () => {
    saving.value = true

    try {
        const payload = {
            ...form.value,
            monthly_fee: form.value.monthly_fee || null
        }

        await api.post('/api/tutors/', payload)

        $q.notify({
            type: 'positive',
            message: 'Tutor successfully added!'
        })

        dialog.value = false
        form.value = emptyForm()

        await fetchTutors()
    } catch (error) {
        console.error('Error saving tutor:', error)

        $q.notify({
            type: 'negative',
            message:
                error.response?.data?.detail ||
                'Tutor save nahi ho saka. Backend check karein.'
        })
    } finally {
        saving.value = false
    }
}

// Show tutor details
const showDetails = (tutor) => {
    selectedTutor.value = tutor
    detailsDialog.value = true
}

// Generate initials
const getInitials = (name) => {
    return (name || 'T')
        .split(' ')
        .filter(Boolean)
        .map(word => word[0])
        .join('')
        .slice(0, 2)
        .toUpperCase()
}

// Format monthly fee
const formatFee = (fee) => {
    if (fee === null || fee === undefined) return 'Not added'

    return `Rs. ${Number(fee).toLocaleString('en-PK')}`
}

// Load data when page opens
onMounted(() => {
    fetchTutors()
})
</script>

<style scoped>
.q-page {
    background: aliceblue;
}
.stat-card {
    border-radius: 12px;
}

.tutor-card {
    border-radius: 12px;
    transition: 0.2s ease;
}

.tutor-card:hover {
    border-color: #d4a72c;
    transform: translateY(-2px);
}
</style>
