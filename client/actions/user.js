import { LOGIN_SUCCESS, LOGOUT_SUCCESS } from 'constants/user'
import Cookies from 'js-cookie'
import Router from 'next/router'

export const handleLogin = (data, token = null) => {
  if (token) {
    Cookies.set('token', token, { expires: 1 })
  }
  return { type: LOGIN_SUCCESS, payload: data }
}

export const handleLogout = () => {
  Cookies.remove('token')
  Router.push('/login')
  return { type: LOGOUT_SUCCESS }
}
