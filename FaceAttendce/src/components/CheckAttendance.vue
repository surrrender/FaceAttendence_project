<template>
  <div class="container">
    <div class="block">
      <!-- <span class="demonstration">Use value-format</span> -->
      <!-- <div class="demonstration">Value：{{ value2 }}</div> -->
      <!-- <el-date-picker
        v-model="value2"
        type="datetime"
        placeholder="请选择检查考勤的时间"
        format="YYYY/MM/DD hh:mm:ss"
        value-format="YYYY/MM/DD hh:mm:ss a"
      /> -->
      <el-date-picker
        v-model="value2"
        type="datetime"
        placeholder="Pick a Date"
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
import { ref, computed } from "vue";
import axios from "axios";
import { decode } from "base-64";

const faceEncodings = ref([]); // 存储从后端返回的人脸编码
const currentFaceIndex = ref(0);

const dialogVisible = ref(false);
const TableData = ref([]);
const value2 = ref("");

const baseURL = import.meta.env.VITE_API_BASE_URL;

// const formattedAbsentNames = computed(() => {
//   return absent_names.value.map(name => ({ name }));
// });

const customUpload = async (options) => {
  const { file } = options;
  try {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("time", value2.value);
    const response = await axios.post(`${baseURL}FA/check_attendance/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
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

<style>
.container {
  display: flex;
  flex-direction: column;
}
.upload-demo {
  /* display: flex;
      flex-direction: column; */
  width: 1000px;
}
.el-icon--upload {
  height: 500px;
}
</style>
