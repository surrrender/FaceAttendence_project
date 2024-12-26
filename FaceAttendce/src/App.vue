<script setup>
import { useRouter } from 'vue-router';
import Login from './components/Login.vue';
import {ref} from 'vue';
const router = useRouter();
const goToRegisterFaces = () => {
  router.push('/RegisterFaces')
}
const goToCheckAttendance = () => {
  router.push('/CheckAttendance')
}
const goToAttendanceInformation =()=>{
  router.push('/AttendanceInformation')
}
const goToLogin = () => {
  router.push('/Login')
}

//用来管理登录窗口是否可见
const dialogVisible = ref(false);
const closeDialog = () => {
  dialogVisible.value = false;
  console.log("说明在login中传送来了调用次函数的信息")
};
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <el-button color="#626aef" :dark="isDark" size="large" style="font-size: 16px;" @click="dialogVisible=true">登录</el-button>
        <el-dialog class="dialog" v-model="dialogVisible" width="480" :modal="false" align-center>
          <Login @closeDialog="closeDialog"></Login>
        </el-dialog>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu background-color="rgb(242, 202, 152)" style="font-size: 16px;">
            <el-menu-item index="1" @click="goToRegisterFaces">
              <template #title>注册人脸</template>
            </el-menu-item>

            <el-menu-item index="2" @click="goToCheckAttendance">
              <template #title>检查考勤</template>
            </el-menu-item>

            <el-menu-item index="3" @click="goToAttendanceInformation">
              <template #title>查看考勤信息</template>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <router-view></router-view>
      </el-container>
    </el-container>
  </div>
</template>

<style>
.el-menu {
  background-color: rgb(242, 202, 152);
}

.el-aside {
  background-color: rgb(242, 202, 152);
}

.common-layout {
  height: 100vh;
  /* 设置整个布局的高度为视口高度 */
}

.el-container {
  background-color: bisque;
  height: 100%;
  display: flex;
}

.el-header {
  background-color: rgb(174, 167, 244);
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.common-layout .dialog {
  height: auto;
  background-color: rgb(229, 225, 221);
}
</style>
