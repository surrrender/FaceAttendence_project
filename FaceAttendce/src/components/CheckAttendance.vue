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
        v-model="value2"
        type="datetime"
        placeholder="请选择查看考勤的具体时间"
        format="YYYY-MM-DD HH:mm"
        date-format="YYYY/MM/DD"
        time-format="HH:mm"
        value-format="YYYY/MM/DD HH:mm"
      />
    </div>
    <el-upload
      class="upload-demo"
      drag
      :http-request="customUpload"
      action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
      multiple
      @success="handleSuccess"
      @error="handleError"
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">拖动文件到这儿 or <em>点击上传文件</em></div>
      <template #tip>
        <div class="el-upload__tip">jpg/png files with a size less than 500kb</div>
      </template>
    </el-upload>

    <!-- 弹窗展示缺席人员 -->
    <el-dialog v-model="dialogVisible" title="缺席人员名单">
      <el-table :data="TableData" style="width: 100%">
        <el-table-column label="Name" prop="name"></el-table-column>
        <el-table-column label="Time" prop="time"></el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script setup>
import { UploadFilled } from "@element-plus/icons-vue";
import { ref, computed,onMounted } from "vue";
import axios from "axios";
import { decode } from "base-64";

const faceEncodings = ref([]); // 存储从后端返回的人脸编码
const currentFaceIndex = ref(0);

const dialogVisible = ref(false);
const TableData = ref([]);
const value2 = ref("");
const lectureName = ref('');
const baseURL = import.meta.env.VITE_API_BASE_URL;


const lectureNames = ref([]);
onMounted(async () => {
  try {
    const baseURL = import.meta.env.VITE_API_BASE_URL;
    const token = localStorage.getItem('token');
    const response = await axios.get(`${baseURL}FA/require_lectures/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    lectureNames.value = response.data.lectureNames;
    console.log(lectureNames.value);
  } catch(error) {
    console.error('获取课程数据错误',error);
  }
});

const customUpload = async (options) => {
  const { file } = options;
  try {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("time", value2.value);
    formData.append("lecture_name",lectureName.value);
    const token = localStorage.getItem('token');
    const response = await axios.post(`${baseURL}FA/check_attendance/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        'Authorization': `Token ${token}`,  
        },
    });
    console.log("Upload success:", response.data.message);
    console.log(response.data.absent_names);
    TableData.value = response.data.absent_names;

    //显示弹窗
    dialogVisible.value = true;
  } catch (error) {
    options.onError(error);
  }
};
</script>

<style scoped>
.el-date-picker{
  margin-left: 20px;
}
      

.container {
  display: flex;
  flex-direction: column;
}
.upload-demo {
  width: 1000px;
  background-color: rgb(248, 232, 213);
}
.el-icon--upload {
  height: 500px;
}
</style>
