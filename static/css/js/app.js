async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        credentials: "include",
        ...options
    });

    let data = null;

    try {
        data = await response.json();
    } catch (error) {
        data = null;
    }

    if (!response.ok) {
        const message =
            data?.detail ||
            data?.message ||
            "Something went wrong.";

        throw new Error(message);
    }

    return data;
}


function formatCurrency(value) {
    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0
    }).format(Number(value) || 0);
}


function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}


function showLoading(element, message = "Generating recommendations...") {
    element.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <h3>${escapeHtml(message)}</h3>
            <p>Please wait.</p>
        </div>
    `;
}


function renderRecommendations(container, data) {
    const recommendations = data.recommendations || [];
    const allocations = data.allocations || {};

    let allocationsHtml = "";

    for (const [key, value] of Object.entries(allocations)) {
        allocationsHtml += `
            <div class="allocation-item">
                <span>${escapeHtml(key)}</span>
                <strong>${formatCurrency(value)}</strong>
            </div>
        `;
    }


    let recommendationsHtml = "";

    recommendations.forEach(item => {
        recommendationsHtml += `
            <article class="recommendation-card">

                <div class="recommendation-top">

                    <span class="recommendation-category">
                        ${escapeHtml(item.category)}
                    </span>

                    <span class="platform">
                        ${escapeHtml(item.platform)}
                    </span>

                </div>

                <h3>
                    ${escapeHtml(item.name)}
                </h3>

                <div class="price">
                    ${formatCurrency(item.estimated_price)}
                </div>

                <p>
                    ${escapeHtml(item.reason)}
                </p>

                ${
                    item.url
                    ? `
                    <a
                        href="${escapeHtml(item.url)}"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="text-link"
                    >
                        Visit platform →
                    </a>
                    `
                    : ""
                }

            </article>
        `;
    });


    const notesHtml =
        (data.notes || [])
        .map(note => `<li>${escapeHtml(note)}</li>`)
        .join("");


    container.innerHTML = `

        <div class="result-header">

            <div>

                <span class="badge">
                    ${data.ai_generated ? "Gemini AI" : "Fallback Engine"}
                </span>

                <h2>
                    Your recommendations
                </h2>

            </div>

            <div class="result-budget">
                ${formatCurrency(data.budget)}
            </div>

        </div>


        <div class="summary-box">

            <p>
                ${escapeHtml(data.summary)}
            </p>

        </div>


        <h3 class="result-section-title">
            Budget Allocation
        </h3>

        <div class="allocation-list">
            ${allocationsHtml}
        </div>


        <h3 class="result-section-title">
            Recommendations
        </h3>

        <div class="recommendation-grid">
            ${recommendationsHtml}
        </div>


        ${
            notesHtml
            ? `
                <div class="notes-box">

                    <strong>
                        Notes
                    </strong>

                    <ul>
                        ${notesHtml}
                    </ul>

                </div>
            `
            : ""
        }

    `;
}


const homeForm = document.getElementById("homeForm");

if (homeForm) {

    homeForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const results = document.getElementById("homeResults");

        showLoading(results);

        const roomElements =
            document.querySelectorAll(
                'input[name="rooms"]:checked'
            );

        const rooms =
            Array.from(roomElements)
            .map(element => element.value);


        if (rooms.length === 0) {
            results.innerHTML = `
                <div class="alert error">
                    Please select at least one room.
                </div>
            `;
            return;
        }


        const payload = {

            budget:
                Number(
                    document.getElementById(
                        "homeBudget"
                    ).value
                ),

            rooms: rooms,

            style:
                document.getElementById(
                    "homeStyle"
                ).value,

            items: {

                lights:
                    Number(
                        document.getElementById(
                            "lights"
                        ).value
                    ),

                ceiling_fans:
                    Number(
                        document.getElementById(
                            "fans"
                        ).value
                    ),

                dining_tables:
                    Number(
                        document.getElementById(
                            "diningTables"
                        ).value
                    ),

                wall_art:
                    Number(
                        document.getElementById(
                            "wallArt"
                        ).value
                    )
            }
        };


        try {

            const data =
                await apiRequest(
                    "/generate-home",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(payload)
                    }
                );

            renderRecommendations(
                results,
                data
            );

        } catch (error) {

            results.innerHTML = `
                <div class="alert error">
                    ${escapeHtml(error.message)}
                </div>
            `;
        }

    });
}


const partyForm = document.getElementById("partyForm");

if (partyForm) {

    partyForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const results =
            document.getElementById(
                "partyResults"
            );

        showLoading(results);


        const payload = {

            budget:
                Number(
                    document.getElementById(
                        "partyBudget"
                    ).value
                ),

            guests:
                Number(
                    document.getElementById(
                        "partyGuests"
                    ).value
                ),

            event_type:
                document.getElementById(
                    "eventType"
                ).value,

            venue:
                document.getElementById(
                    "partyVenue"
                ).value,

            preferences:
                document.getElementById(
                    "partyPreferences"
                ).value
        };


        try {

            const data =
                await apiRequest(
                    "/generate-party",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(payload)
                    }
                );

            renderRecommendations(
                results,
                data
            );

        } catch (error) {

            results.innerHTML = `
                <div class="alert error">
                    ${escapeHtml(error.message)}
                </div>
            `;
        }

    });
}


const jewelryForm =
    document.getElementById(
        "jewelryForm"
    );


if (jewelryForm) {

    jewelryForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const results =
                document.getElementById(
                    "jewelryResults"
                );

            showLoading(results);


            const formData =
                new FormData();


            formData.append(
                "budget",
                document.getElementById(
                    "jewelryBudget"
                ).value
            );


            formData.append(
                "occasion",
                document.getElementById(
                    "occasion"
                ).value
            );


            formData.append(
                "style",
                document.getElementById(
                    "jewelryStyle"
                ).value
            );


            formData.append(
                "outfit_description",
                document.getElementById(
                    "outfitDescription"
                ).value
            );


            const imageInput =
                document.getElementById(
                    "outfitImage"
                );


            if (
                imageInput.files &&
                imageInput.files.length > 0
            ) {

                formData.append(
                    "outfit_image",
                    imageInput.files[0]
                );
            }


            try {

                const data =
                    await apiRequest(
                        "/generate-jewelry",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                renderRecommendations(
                    results,
                    data
                );

            } catch (error) {

                results.innerHTML = `
                    <div class="alert error">
                        ${escapeHtml(error.message)}
                    </div>
                `;
            }

        }
    );
}


async function viewHistory(id) {

    try {

        const data =
            await apiRequest(
                `/recommendations-details/${id}`
            );


        const container =
            document.getElementById(
                "historyDetails"
            );


        container.innerHTML = `

            <span class="badge">
                ${escapeHtml(
                    data.planner_type.toUpperCase()
                )}
            </span>

            <h2>
                Recommendation #${data.id}
            </h2>

            <h3>
                Request
            </h3>

            <pre>${escapeHtml(
                JSON.stringify(
                    data.request,
                    null,
                    2
                )
            )}</pre>


            <h3>
                Response
            </h3>

            <pre>${escapeHtml(
                JSON.stringify(
                    data.response,
                    null,
                    2
                )
            )}</pre>

        `;


        document
            .getElementById(
                "historyModal"
            )
            .classList.remove(
                "hidden"
            );

    } catch (error) {

        alert(error.message);
    }
}


function closeModal() {

    const modal =
        document.getElementById(
            "historyModal"
        );

    if (modal) {
        modal.classList.add(
            "hidden"
        );
    }
}


document.addEventListener(
    "click",
    function(event) {

        const modal =
            document.getElementById(
                "historyModal"
            );

        if (
            modal &&
            event.target === modal
        ) {
            closeModal();
        }

    }
);