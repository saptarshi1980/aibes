import api from "../api/api";

export async function getAllTenders() {

    const response = await api.get("/tenders");

    return response.data;

}

export async function getTender(id) {

    const response = await api.get("/tenders/" + id);

    return response.data;

}

export async function getTenderDocuments(tenderId) {

    const response = await api.get(
        "/tenders/" + tenderId + "/documents"
    );

    return response.data;

}

export async function getCriteria(tenderId) {

    const response = await api.get(
        "/criteria/" + tenderId
    );

    return response.data;

}

export async function getBidders(tenderId) {

    const response = await api.get(
        "/bidders/tender/" + tenderId
    );

    return response.data;

}

export async function getBidder(bidderId) {

    const response = await api.get(
        "/bidders/" + bidderId
    );

    return response.data;

}

export async function getEvaluationResults(
    bidderId
) {

    const response = await api.get(
        "/evaluation/bidder/" + bidderId
    );

    return response.data;

}

export async function createTender(data) {
    const response = await api.post("/tenders", data);
    return response.data;
}

export async function updateTender(id, data) {
    const response = await api.put(`/tenders/${id}`, data);
    return response.data;
}

export async function uploadTenderDocument(
    tenderId,
    formData
) {

    const response = await api.post(

        `/tenders/${tenderId}/documents`,

        formData,

        {

            headers: {

                "Content-Type": "multipart/form-data"

            }

        }

    );

    return response.data;

}

export async function getBidderDocuments(bidderId) {

    const response = await api.get(

        "/bidders/" + bidderId + "/documents"

    );

    return response.data;

}

export async function uploadBidderDocument(
    bidderId,
    formData
) {

    const response = await api.post(

        "/bidders/" + bidderId + "/documents",

        formData,

        {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }

    );

    return response.data;

}

export async function evaluateBidder(bidderId) {

    const response = await api.post(

        "/evaluation/bidder/" + bidderId

    );

    return response.data;

}

export async function extractCriteria(tenderId) {

    const response = await api.post(
        "/criteria/extract/" + tenderId
    );

    return response.data;

}

