<template>
    <Modal v-model="show">
    </Modal>
</template>

<script>
import Modal from '@/components/Modal';

export default {
    components:{
        Modal
    },
    props: ["value"],
    data() {
        return {
            show: false
        }
    },
    watch: {
        value() {
            this.show = this.value != null;
        },
        show() {
            if(!this.show) 
                this.$emit("input", null)
        }
    }
}
</script>

<style>

</style>