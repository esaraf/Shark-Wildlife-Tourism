library(tidyverse)
library(likert)
library(scales)

## Load the Data 
data <- readxl::read_excel("/Users/elizabethsaraf/Desktop/SWT/CSV/raw_data/Response/MasterSheet.xlsx")
colnames(data)

## Adjust N for each group

# Normalize based on sample size 
normalize_data <- function(x){
  
}

# Positive Recode 
likert_factor_recode <- function(x){ # FACTOR
  as.factor(x)
}

likert_recode_agreement_positive_f <- function(x) { # FACTOR
  as.factor(case_when(
    x == 5 ~ "Strongly Agree",
    x == 4 ~ "Agree",
    x == 3 ~ "Unsure",
    x == 2 ~ "Disagree",
    x == 1 ~ "Strongly Disagree",
  ))
}

likert_agreement_recode_n <- function(x){ # NUMERIC
  as.numeric(case_when(
    x == "Strongly Disagree" ~ 1,
    x == "Disagree" ~ 2,
    x == "Unsure" ~ 3,
    x == "Agree" ~ 4,
    x == "Strongly Agree" ~ 5,
  ))
}

# Negative Recode 
likert_recode_agreement_negative_f <- function(x) { # FACTOR
  as.factor(case_when(
    x == 5 ~ "Strongly Disagree",
    x == 4 ~ "Disagree",
    x == 3 ~ "Unsure",
    x == 2 ~ "Agree",
    x == 1 ~ "Strongly Agree",
  ))
}

likert_recode_agreement_negative_n <- function(x) { # NUMERIC
  as.numeric(case_when(
    x == "Strongly Disagree" ~ 5,
    x == "Disagree" ~ 4,
    x == "Unsure" ~ 3,
    x == "Agree" ~ 3,
    x == "Strongly Agree" ~ 1,
  ))
}


# Apply Recoding 
env_id <- data %>%
  select("Timestamp", "SurveyID", "2_3A", "2_3B", "2_3C", "2_3D", "2_3E", "2_3F")

env_id_positive <- env_id %>%
  select(-"Timestamp", -"SurveyID", -"2_3B", -"2_3F") %>%
  mutate_all(likert_agreement_recode_n)

env_id_negative <- env_id %>%
  select("2_3B", "2_3F") %>%
  mutate_all(likert_recode_agreement_negative_n)

# Recombine Data Tables 
env_id_recoded <- cbind(env_id_positive, env_id_negative)

#### Calculate Totals ####
# Overall Total
env_id_recoded$total <- rowSums(env_id_recoded) 

env_id_recoded <- cbind(group = data$SurveyID, env_id_recoded)

# Calculate the median ( lower - less likely to ... higher - more likely to)
env_id_recoded$median <- apply(env_id_recoded[, c("2_3A", "2_3B", "2_3C", "2_3D", "2_3E", "2_3F")], 1, median)

## Reshape data 
long_data <- env_id_recoded %>%
  pivot_longer(data = .,
               cols=2:7,
               names_to="question",
               values_to="response") %>%
  select(-total, -median, group) %>%
  mutate(condition = str_match(group, "^[^_]+(?=_)"),
         trial = str_match(group, "[0-9]$"))

# Aggregate 
long_data %>%
  group_by(group) %>%
  summarise(
    median_response=median(response, na.rm=TRUE), 
    sd_response =sd(response, na.rm=TRUE))

## Score Perception of Sharks
group_sizes <- data.frame(
  group = c("Control_T0", "Control_T2", "Shark_T0", "Shark_T1", "Documentary_T0", "Documentary_T1", "Documentary_T2"),
  size = as.numeric(c("48", "18", "18", "14", "28", "18", "8"))
)

perception_score <- long_data %>%
  group_by(group) %>%
  summarise(
    total_score = as.numeric(sum(response, na.rm=TRUE)),
    median_score = median(response, na.rm=TRUE),
    standard_deviation = round(sd(response, na.rm=TRUE), digits=3),
    .groups = "drop"
  ) %>%
  left_join(group_sizes, by="group")

# Normalize 
perception_score_normalized <- perception_score %>%
  mutate(
    normalized_score = round(as.numeric(total_score / size), digits=3)
  )

# Add a column to extract the time points (T0, T1, T2) from the group column
perception_score_normalized <- perception_score_normalized %>%
  mutate(
    time_point = sub(".*_(T\\d)", "\\1", group),  # Extract T0, T1, T2
    group_type = sub("_T\\d", "", group)          # Extract Control, Shark, Documentary
  )

# Create the bar chart
ggplot(perception_score_normalized, aes(x = time_point, y = normalized_score, fill = group_type)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.9)) +
  scale_fill_manual(
    values = c("Control"="lightblue", "Documentary"="blue", "Shark"="darkblue")
  ) +
  labs(
    title = "Normalized Perception Scores Over Time",
    x = "Time Point",
    y = "Normalized Perception Score",
    fill = "Group"
  ) +
  theme_minimal() +
  theme(
    legend.position = "top",
    axis.text.x = element_text(angle = 45, hjust = 1)
  )


# Plot By Condition and Trial (shark, documentary, control)

ggplot(long_data, aes(x=response)) +
  geom_bar() +
  facet_wrap(~group) +
  coord_flip()
  
ggplot(long_data, aes(x=response)) +
  geom_bar() +
  facet_wrap(~question, nrow =3)

# Create separate data frames for each condition
shark_df <- long_data %>% filter(condition[,1] == "Shark")
doc_df <- long_data %>% filter(condition[,1] == "Documentary")
con_df <- long_data %>% filter(condition[,1] == "Control")

# Summarize our data
shark_group_summary <- long_data %>%
  filter(!is.na(response)) %>%
  group_by(question, response) %>%
  count(name = "n_answers") %>%
  group_by(question) %>%
  mutate(percent_answers = n_answers / sum(n_answers)) %>%
  ungroup() %>%
  mutate(percent_answers_label = percent(percent_answers, accuracy=1)) %>%
  mutate(negative_answers=if_else(response %in% c("3"), n_answers/2, n_answers)) %>%
  mutate(negative_answers=if_else(response %in% c("1", "2"), n_answers, 0)) %>%
  mutate(total_negative_answers=sum())


# Add initial order to divide between opinion and unsure 
shark_group_summary_diverging <- shark_group_summary %>%
  mutate(percent_answers=if_else(response %in% c("3","4", "5"), percent_answers, -percent_answers)) %>%
  mutate(percent_answers_label = percent(percent_answers, accuracy = 1))

# Adjust positive/negative labels 
shark_group_summary_diverging_good_labels <- shark_group_summary_diverging %>%
  mutate(percent_answers_label=abs(percent_answers)) %>%
  mutate(percent_answers_label = percent(percent_answers_label, accuracy = 1))

# Reorder bars 
shark_group_summary_response_as_factor <- shark_group_summary_diverging_good_labels %>%
  mutate(
    response =if_else(
      question %in% c("2_3B", "2_3F"), 
      likert_recode_agreement_negative_f(response), 
      likert_recode_agreement_positive_f(response)))

shark_group_summary_right_order <- shark_group_summary_response_as_factor %>%
  mutate(response = fct_relevel(response, "Strongly Disagree", "Disagree", "Unsure", "Agree", "Strongly Agree"),
         response = fct_rev(response))

# Rename questions to reflect actual variable names 
summary <- shark_group_summary_right_order %>%
  mutate(question = case_when(
    question == "2_3A" ~ "I like to learn about sharks",
    question == "2_3B" ~ "I think feeding sharks makes them associate humans with rewards",
    question == "2_3C" ~ "I think Sharks are critical to the marine environment",
    question == "2_3D" ~ "I think Sharks need more legal protection",
    question == "2_3E" ~ "I think Sharks should not be harvested",
    question == "2_3F" ~ "I think Protection laws have caused shark overpopulation",
  ))


summary %>%
  ggplot(aes(x=question,
             y=percent_answers,
             fill=response)) +
  geom_col() +
  geom_text(aes(label = percent_answers_label),
            position = position_stack(vjust = 0.5),
            color = "black",
            
            fontface = "bold") +
  coord_flip () +
  scale_x_discrete() +
  scale_fill_brewer(palette = "RdYlBu") +
  labs(
       x = NULL,
       fill = NULL) +
  theme_minimal() +
  theme(axis.text.x=element_blank(),
        axis.title.x=element_blank(),
        legend.position="top") 























