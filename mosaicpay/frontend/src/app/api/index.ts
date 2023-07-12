//TODO FETCH ROOT ROUTE FROM ENV

import axios from "axios";
import { dtoRegister } from "../dtos/dtoRegistser";
import { dtoLogin } from "../dtos/dtoLogin";

const rootRoute = process.env.NEXT_PUBLIC_API_URL;

export const register = (dtoRegister: dtoRegister) =>
	axios.post(`${rootRoute}auth/register`, dtoRegister).then((res) => res.data);

export const login = (dtoLogin: dtoLogin) =>
	axios.post(`${rootRoute}auth/login`, dtoLogin).then((res) => res.data);
export const logout = () =>
	axios
		.post(`${rootRoute}auth/logout`, {}, { withCredentials: true })
		.then((res) => res.data);

export const getUserAccounts = () =>
	axios
		.get(`${rootRoute}account/`, { withCredentials: true })
		.then((res) => res.data);

export const getAccount = (accountId: number) =>
	axios
		.get(`${rootRoute}account/${accountId}`, { withCredentials: true })
		.then((res) => res.data);

export const postNewAccount = (dtoAccount: dtoAccount) =>
	axios
		.post(`${rootRoute}account/`, dtoAccount, { withCredentials: true })
		.then((res) => res.data);

export const putAccount = (
	accountId: number,
	dtoAccountUpdate: dtoAccountUpdate
) =>
	axios
		.put(`${rootRoute}account/${accountId}/`, dtoAccountUpdate, {
			withCredentials: true,
		})
		.then((res) => res.data);

export const getUser = () =>
	axios
		.get(`${rootRoute}auth/get-user`, { withCredentials: true })
		.then((res) => res.data);

export const postNewTransaction = (dtoTransaction: dtoTransaction) =>
	axios
		.post(`${rootRoute}transaction/`, dtoTransaction, {
			withCredentials: true,
		})
		.then((res: any) => res.data);
export const deleteAccount = (accountId: string | string[] | undefined) =>
	axios
		.delete(`${rootRoute}account/${accountId}/`, { withCredentials: true })
		.then((res) => res.data);

export const putTransaction = (
	transactionId: string | string[] | undefined,
	dtoTransactionUpdate: dtoTransactionUpdate
) =>
	axios
		.put(`${rootRoute}transaction/${transactionId}/`, dtoTransactionUpdate, {
			withCredentials: true,
		})
		.then((res) => res.data);
export const getTransaction = (transactionId: string | string[] | undefined) =>
	axios
		.get(`${rootRoute}transaction/${transactionId}`, { withCredentials: true })
		.then((res) => res.data);
export const deleteTransaction = (
	transactionId: string | string[] | undefined
) =>
	axios
		.delete(`${rootRoute}transaction/${transactionId}/`, {
			withCredentials: true,
		})
		.then((res) => res.data);

export const getAccountsTransactions = () =>
	axios
		.get(`${rootRoute}transaction`, {
			withCredentials: true,
		})
		.then((res) => res.data);
export const postDocument = (document: any) =>
	axios
		.post(`${rootRoute}document/`, document, {
			withCredentials: true,
			headers: { "Content-Type": "multpart/form-data" },
		})
		.catch((res: any) => res.data);
export const putDocument = (documentId: string | undefined, document: any) =>
	axios
		.put(`${rootRoute}document/${documentId}/`, document, {
			withCredentials: true,
			headers: { "Content-Type": "multpart/form-data" },
		})
		.catch((res: any) => res.data);
export const getDocument = (accountId: string | string[]) =>
	axios
		.get(`${rootRoute}document/${accountId}`, {
			withCredentials: true,
		})
		.then((res: any) => res.data);
