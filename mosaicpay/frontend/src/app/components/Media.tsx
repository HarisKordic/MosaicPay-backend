import { Alert, Box, Button, ImageList, ImageListItem } from "@mui/material";
import { useEffect, useState } from "react";
import UploadOutlinedIcon from "@mui/icons-material/UploadOutlined";
import LoadingButton from "@mui/lab/LoadingButton";
import { postDocument, putDocument } from "../api";

interface IProps {
	accountId: string;
	userId: string;
	url?: string;
	type: string;
	isInitial?: boolean;
	documentId?: number;
}
export default function Media(props: IProps) {
	const [maxUploadNumReached, setMaxUploadNumReached] = useState(false);
	const [isSavingLoading, setIsSavingLoading] = useState(false);
	const [url, setUrl] = useState(props.url);
	const [type, setType] = useState(props.type);
	const [documentId, setDocumentId] = useState(props.documentId);
	const [userId, setUserId] = useState(props.userId);

	const handleFileUpload = async (event: any) => {
		uploadImages(event.target.files);
	};
	const uploadImages = async (file: any) => {
		setIsSavingLoading(true);

		try {
			let form = new FormData();
			form.append("url", file[0]);
			form.append("type", file[0].type.split("/")[1]);
			form.append("user", userId);
			form.append("account", props.accountId);

			let result;
			if (documentId === 0) {
				result = await postDocument(form);
			} else {
				result = await putDocument(documentId?.toString(), form);
			}

			setDocumentId(result.data?.document_id);
			setUrl(result.data?.url);
			setType(result.data?.type);
		} catch (error: any) {
			if (error.response.status === 405) {
				setMaxUploadNumReached(true);
			}
		} finally {
			setIsSavingLoading(false);
		}
	};

	useEffect(() => {
		setUrl(props?.url);
		setType(props?.type);
		setDocumentId(props.documentId);
		setUserId(props.userId);
	}, [props.type, props.url, props.documentId, props.userId]);

	return (
		<Box
			sx={{
				display: "flex",
				justifyContent: "center",
				flexDirection: "column",
			}}
		>
			{maxUploadNumReached ? (
				<Alert severity="error">Reached maximum of 10 files per product!</Alert>
			) : (
				<LoadingButton
					sx={{
						my: 1,
					}}
					loading={isSavingLoading}
					loadingPosition="start"
					startIcon={<UploadOutlinedIcon />}
					variant="outlined"
					component="label"
					color="secondary"
				>
					Upload media
					<input
						hidden
						accept=".jpeg, .jpg, .pdf"
						type="file"
						onChange={(e: any) => handleFileUpload(e)}
					/>
				</LoadingButton>
			)}
			{type !== "pdf" ? (
				<ImageList
					variant="quilted"
					sx={{
						p: 1,
						display: "flex",
						justifyContent: "center",
						flexWrap: "wrap",
					}}
				>
					<ImageListItem key={1}>
						<img
							style={{
								display: `${
									type === "jpg" || type === "jpeg" ? "flex" : "none"
								}`,
							}}
							src={url}
							alt={"Asset"}
							loading="lazy"
						/>
					</ImageListItem>
				</ImageList>
			) : (
				<Box
					sx={{
						p: 1,
						display: "flex",
						justifyContent: "center",
					}}
				>
					<Button
						color="secondary"
						sx={{
							display: `${type === "pdf" ? "flex" : "none"}`,
						}}
						onClick={() => window.open(url, "_blank")}
					>
						View PDF
					</Button>
				</Box>
			)}
		</Box>
	);
}
