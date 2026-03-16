# emailer/send_email.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL, YOUR_NAME, TOP_N_RESULTS


def send_email(subject, html_body):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Internship Agent <{GMAIL_ADDRESS}>"
        msg["To"] = RECIPIENT_EMAIL
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

        print(f"Email sent to {RECIPIENT_EMAIL}!")
        return True

    except Exception as e:
        print(f"Email error: {e}")
        return False


def build_digest_email(scored_companies):
    top = scored_companies[:TOP_N_RESULTS]

    cards = ""
    for i, company in enumerate(top, 1):
        score = company["match_score"]

        if score >= 8:
            score_bg = "#dcfce7"
            score_color = "#16a34a"
            score_border = "#16a34a"
            badge_label = "Strong Match"
        elif score >= 6:
            score_bg = "#fef9c3"
            score_color = "#ca8a04"
            score_border = "#ca8a04"
            badge_label = "Good Match"
        else:
            score_bg = "#fee2e2"
            score_color = "#dc2626"
            score_border = "#dc2626"
            badge_label = "Weak Match"

        cards += f"""
        <tr>
          <td style="padding:0 0 20px 0;">
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="background:#ffffff; border:1px solid #e2e8f0;
                          border-radius:16px; overflow:hidden;
                          box-shadow:0 1px 4px rgba(0,0,0,0.06);">
              <!-- Card Header -->
              <tr>
                <td style="background:linear-gradient(135deg,#1e1b4b,#3730a3);
                           padding:18px 24px;">
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td>
                        <span style="font-size:11px; color:#a5b4fc;
                                     text-transform:uppercase;
                                     letter-spacing:1px;
                                     font-family:Arial,sans-serif;">
                          Opportunity #{i}
                        </span>
                        <br/>
                        <span style="font-size:20px; font-weight:700;
                                     color:#ffffff;
                                     font-family:Arial,sans-serif;">
                          {company['name']}
                        </span>
                      </td>
                      <td align="right">
                        <div style="background:{score_bg};
                                    border:1px solid {score_border};
                                    border-radius:50px; padding:6px 14px;
                                    display:inline-block;">
                          <span style="color:{score_color};
                                       font-weight:700; font-size:13px;
                                       font-family:Arial,sans-serif;">
                            {score}/10 &bull; {badge_label}
                          </span>
                        </div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- Card Body -->
              <tr>
                <td style="padding:20px 24px;">
                  <table width="100%" cellpadding="0" cellspacing="0">

                    <!-- Roles -->
                    <tr>
                      <td style="padding-bottom:12px;">
                        <table cellpadding="0" cellspacing="0">
                          <tr>
                            <td style="background:#ede9fe; border-radius:6px;
                                       padding:4px 10px;">
                              <span style="font-size:11px; color:#6d28d9;
                                           font-weight:700;
                                           font-family:Arial,sans-serif;
                                           text-transform:uppercase;
                                           letter-spacing:0.5px;">
                                &#128188; Roles
                              </span>
                            </td>
                          </tr>
                        </table>
                        <p style="margin:6px 0 0; font-size:14px;
                                  color:#1e293b; font-family:Arial,sans-serif;
                                  line-height:1.5;">
                          {company['roles']}
                        </p>
                      </td>
                    </tr>

                    <!-- Skill Gaps -->
                    <tr>
                      <td style="padding-bottom:12px;">
                        <table cellpadding="0" cellspacing="0">
                          <tr>
                            <td style="background:#fef3c7; border-radius:6px;
                                       padding:4px 10px;">
                              <span style="font-size:11px; color:#b45309;
                                           font-weight:700;
                                           font-family:Arial,sans-serif;
                                           text-transform:uppercase;
                                           letter-spacing:0.5px;">
                                &#9889; Skill Gaps
                              </span>
                            </td>
                          </tr>
                        </table>
                        <p style="margin:6px 0 0; font-size:14px;
                                  color:#1e293b; font-family:Arial,sans-serif;
                                  line-height:1.5;">
                          {company['skill_gaps']}
                        </p>
                      </td>
                    </tr>

                    <!-- Deadline -->
                    <tr>
                      <td style="padding-bottom:16px;">
                        <table cellpadding="0" cellspacing="0">
                          <tr>
                            <td style="background:#fee2e2; border-radius:6px;
                                       padding:4px 10px;">
                              <span style="font-size:11px; color:#b91c1c;
                                           font-weight:700;
                                           font-family:Arial,sans-serif;
                                           text-transform:uppercase;
                                           letter-spacing:0.5px;">
                                &#128197; Deadline
                              </span>
                            </td>
                          </tr>
                        </table>
                        <p style="margin:6px 0 0; font-size:14px;
                                  color:#dc2626; font-weight:600;
                                  font-family:Arial,sans-serif;">
                          {company['deadlines']}
                        </p>
                      </td>
                    </tr>

                    <!-- Summary -->
                    <tr>
                      <td style="padding-bottom:20px;
                                 border-left:3px solid #6366f1;
                                 padding-left:12px;">
                        <p style="margin:0; font-size:13px; color:#475569;
                                  font-style:italic;
                                  font-family:Arial,sans-serif;
                                  line-height:1.6;">
                          {company['summary']}
                        </p>
                      </td>
                    </tr>

                    <!-- Button -->
                    <tr>
                      <td>
                        <table cellpadding="0" cellspacing="0">
                          <tr>
                            <td style="background:#4f46e5; border-radius:8px;">
                              <a href="{company['url']}"
                                 style="display:inline-block; padding:12px 24px;
                                        color:#ffffff; font-weight:700;
                                        font-size:14px; text-decoration:none;
                                        font-family:Arial,sans-serif;">
                                View &amp; Apply &#8594;
                              </a>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>

                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0; padding:0; background:#f1f5f9;">
      <table width="100%" cellpadding="0" cellspacing="0"
             style="background:#f1f5f9; padding:32px 16px;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0">

              <!-- Header -->
              <tr>
                <td style="background:linear-gradient(135deg,#1e1b4b,#4f46e5);
                           border-radius:16px 16px 0 0; padding:32px 32px 28px;
                           text-align:center;">
                  <p style="margin:0 0 4px; font-size:28px;">&#129302;</p>
                  <h1 style="margin:0; font-size:26px; font-weight:800;
                             color:#ffffff; font-family:Arial,sans-serif;">
                    Internship Agent
                  </h1>
                  <p style="margin:8px 0 0; font-size:14px; color:#a5b4fc;
                             font-family:Arial,sans-serif;">
                    Daily Opportunity Digest &bull; Personalized for {YOUR_NAME}
                  </p>
                </td>
              </tr>

              <!-- Summary Bar -->
              <tr>
                <td style="background:#312e81; padding:14px 32px;">
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="text-align:center;">
                        <span style="font-size:13px; color:#c7d2fe;
                                     font-family:Arial,sans-serif;">
                          &#128269; Scanned companies &nbsp;&bull;&nbsp;
                          &#127775; Found <strong
                            style="color:#ffffff;">{len(top)} matches
                          </strong> for your profile today
                        </span>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- Body -->
              <tr>
                <td style="background:#f8fafc; padding:28px 28px 8px;
                           border-radius:0 0 16px 16px;">
                  <table width="100%" cellpadding="0" cellspacing="0">

                    <!-- Greeting -->
                    <tr>
                      <td style="padding-bottom:20px;">
                        <p style="margin:0; font-size:15px; color:#334155;
                                   font-family:Arial,sans-serif;
                                   line-height:1.6;">
                          Hey <strong>{YOUR_NAME}</strong>! &#128075;
                          Here are your top internship matches ranked
                          by how well they fit your skill profile.
                          Don't let the deadlines sneak up on you!
                        </p>
                      </td>
                    </tr>

                    <!-- Opportunity Cards -->
                    {cards}

                    <!-- Bookmark Tip -->
                    <tr>
                      <td style="padding-bottom:24px;">
                        <table width="100%" cellpadding="0" cellspacing="0"
                               style="background:#eff6ff;
                                      border:1px solid #bfdbfe;
                                      border-radius:12px;">
                          <tr>
                            <td style="padding:16px 20px;">
                              <p style="margin:0; font-size:13px;
                                         color:#1e40af;
                                         font-family:Arial,sans-serif;
                                         line-height:1.6;">
                                &#128278; <strong>Bookmark tip:</strong>
                                Reply to this email with
                                <strong>SAVE 1</strong>,
                                <strong>SAVE 2</strong> etc. to bookmark
                                an opportunity. Your agent will send you
                                deadline reminders automatically!
                              </p>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                      <td style="border-top:1px solid #e2e8f0;
                                 padding-top:20px; padding-bottom:8px;
                                 text-align:center;">
                        <p style="margin:0; font-size:12px; color:#94a3b8;
                                   font-family:Arial,sans-serif;">
                          Sent by your personal Internship Agent &#129302;
                          &bull; Built with Python &bull; 100% Free
                        </p>
                      </td>
                    </tr>

                  </table>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """
    return html


def build_reminder_email(bookmarks):
    cards = ""
    for b in bookmarks:
        cards += f"""
        <tr>
          <td style="padding:0 0 20px 0;">
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="background:#ffffff; border:2px solid #f59e0b;
                          border-radius:16px; overflow:hidden;">
              <tr>
                <td style="background:linear-gradient(135deg,#78350f,#d97706);
                           padding:16px 24px;">
                  <span style="font-size:18px; font-weight:700;
                               color:#ffffff; font-family:Arial,sans-serif;">
                    &#9200; {b['company']}
                  </span>
                </td>
              </tr>
              <tr>
                <td style="padding:20px 24px;">
                  <p style="margin:0 0 8px; font-size:14px; color:#1e293b;
                             font-family:Arial,sans-serif;">
                    <strong>Role:</strong> {b['roles']}
                  </p>
                  <p style="margin:0 0 20px; font-size:14px; color:#dc2626;
                             font-weight:600; font-family:Arial,sans-serif;">
                    <strong>Deadline:</strong> {b['deadlines']}
                  </p>
                  <table cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="background:#f59e0b; border-radius:8px;">
                        <a href="{b['url']}"
                           style="display:inline-block; padding:12px 24px;
                                  color:#ffffff; font-weight:700;
                                  font-size:14px; text-decoration:none;
                                  font-family:Arial,sans-serif;">
                          Apply Now &#8594;
                        </a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0; padding:0; background:#f1f5f9;">
      <table width="100%" cellpadding="0" cellspacing="0"
             style="background:#f1f5f9; padding:32px 16px;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0">

              <tr>
                <td style="background:linear-gradient(135deg,#78350f,#f59e0b);
                           border-radius:16px 16px 0 0; padding:32px;
                           text-align:center;">
                  <p style="margin:0 0 4px; font-size:28px;">&#9200;</p>
                  <h1 style="margin:0; font-size:24px; font-weight:800;
                             color:#ffffff; font-family:Arial,sans-serif;">
                    Deadline Reminder!
                  </h1>
                  <p style="margin:8px 0 0; font-size:14px;
                             color:#fef3c7; font-family:Arial,sans-serif;">
                    Don't let these opportunities slip away, {YOUR_NAME}!
                  </p>
                </td>
              </tr>

              <tr>
                <td style="background:#f8fafc; padding:28px;
                           border-radius:0 0 16px 16px;">
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="padding-bottom:20px;">
                        <p style="margin:0; font-size:15px; color:#334155;
                                   font-family:Arial,sans-serif;">
                          Hey <strong>{YOUR_NAME}</strong>! &#128075;
                          You bookmarked
                          <strong>{len(bookmarks)} opportunities</strong>.
                          The deadlines are coming up — time to apply!
                        </p>
                      </td>
                    </tr>
                    {cards}
                    <tr>
                      <td style="border-top:1px solid #e2e8f0;
                                 padding-top:20px; text-align:center;">
                        <p style="margin:0; font-size:12px; color:#94a3b8;
                                   font-family:Arial,sans-serif;">
                          Sent by your personal Internship Agent &#129302;
                        </p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """
    return html


def send_digest(scored_companies):
    if not scored_companies:
        print("No opportunities to email today.")
        return
    html = build_digest_email(scored_companies)
    send_email("🤖 Your Daily Internship Digest", html)


def send_reminders(bookmarks):
    if not bookmarks:
        print("No reminders to send today.")
        return
    html = build_reminder_email(bookmarks)
    send_email("⏰ Internship Deadline Reminder!", html)


if __name__ == "__main__":
    test_opportunities = [
        {
            "name": "Google",
            "roles": "Machine Learning Intern",
            "match_score": 9.0,
            "skill_gaps": "TensorFlow",
            "deadlines": "April 30, 2025",
            "summary": "Excellent match! Your Python and ML skills align perfectly with this role.",
            "url": "https://careers.google.com"
        },
        {
            "name": "Razorpay",
            "roles": "Data Science Intern",
            "match_score": 7.5,
            "skill_gaps": "Apache Spark, Hadoop",
            "deadlines": "May 15, 2025",
            "summary": "Good match overall. Minor gaps in big data tools which you can pick up quickly.",
            "url": "https://razorpay.com/jobs"
        },
        {
            "name": "Swiggy",
            "roles": "AI/ML Intern",
            "match_score": 8.5,
            "skill_gaps": "Computer Vision basics",
            "deadlines": "April 20, 2025",
            "summary": "Strong match! Swiggy is actively hiring ML interns and your profile fits well.",
            "url": "https://careers.swiggy.com"
        }
    ]

    print("Sending improved digest email...")
    send_digest(test_opportunities)