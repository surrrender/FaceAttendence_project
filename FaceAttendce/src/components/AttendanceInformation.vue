<template>
  <div class="container">
    <div class="block">
      <el-select
        v-model="lectureName"
        placeholder="请选择要查看考勤的班级"
        size="large"
        style="width: 240px"
      >
        <el-option
          v-for="item in lectureNames"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-date-picker
        size="large"
        v-model="selectDate"
        type="datetime"
        placeholder="请选择查看考勤的具体时间"
        format="YYYY-MM-DD HH:mm"
        date-format="YYYY/MM/DD"
        time-format="HH:mm"
        value-format="YYYY/MM/DD HH:mm"
      />
      <span slot="footer" class="dialog-footer">
        <el-button @click="sumbit" size="large">查询</el-button>
      </span>
    </div>
    <div class="table" style="width: 800px;height: 800px;">
      <el-table :data="TableData" style="width: 100%" :height="500">
        <el-table-column label="lecture" prop="lecture"></el-table-column>
        <el-table-column label="Name" prop="name"></el-table-column>
        <el-table-column label="Time" prop="time"></el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const TableData = ref([]);
const lectureName = ref("");
const lectureNames = ref([]);
const baseURL = import.meta.env.VITE_API_BASE_URL;
const token = localStorage.getItem("token");

const selectDate = ref("");
onMounted(async () => {
  try {
    // const baseURL = import.meta.env.VITE_API_BASE_URL;
    // const token = localStorage.getItem("token");
    const response = await axios.get(`${baseURL}FA/require_lectures/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    lectureNames.value = response.data.lectureNames;
    console.log(lectureNames.value);
  } catch (error) {
    console.error("获取课程数据错误", error);
  }
});

const sumbit = async () => {
  //不管是否课程和日期信息给传入，都返回对应的数据
  let data = { lectureName: lectureName.value, date: selectDate.value };
  try {
    const response = await axios.post(`${baseURL}FA/show_absent_information/`, data, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    TableData.value = response.data.tableData;
    console.log(TableData.value)
  } catch (error) {
    console.error("发送课程信息和日期出错", error);
  }
};
</script>

<style>
.container {
    display: flex;
    flex-direction: column;
}
.dialog-footer {
    margin-left: 274px;
}
/* .el-table {
    background-color: rgb(248, 232, 213);
} */
</style>