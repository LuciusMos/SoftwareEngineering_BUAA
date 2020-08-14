<template>
  <div class="dashboard-container">
    <div class="dashboard-text">欢迎您， {{ name }}</div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import global from "@/App"

export default {
  data() {
    return {
      name: "Dashboard"
    }
  },
  created() {
    this.axios
      .post(global.server + "admin/get_data/index_info")
      .then(res => {
        console.log(res.data);
        this.name = res.data;
      });
  }
  // computed: {
  //   ...mapGetters([
  //     'name'
  //   ])

  // }
};
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
