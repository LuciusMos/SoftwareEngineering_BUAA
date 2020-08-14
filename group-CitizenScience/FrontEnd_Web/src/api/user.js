import request from '@/utils/request'
import global from "@/App"

export function login(data) {
  return request({
    // url: 'http://114.115.129.146:5000/admin/user_login',
    url: global.server+'admin/user_login',
    method: 'post',
    data
  })
}

export function getInfo(data) {
  return request({
    // url: 'http://114.115.129.146:5000/admin/user_info',
    url: global.server + 'admin/user_info',
    method: 'post',
    data
  })
}

export function logout() {
  return request({
    url: global.server + 'admin/user_logout',
    method: 'post'
  })
}
